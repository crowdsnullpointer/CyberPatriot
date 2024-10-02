import os,subprocess
from os import path
from glob import glob

LIGHT_DM_PATH = "/etc/lightdm/lightdm.conf"
SSHD_PATH = "/etc/ssh/sshd_config"
UPDATE_PACKAGE_LIST_PATH = "/etc/apt/apt.conf.d/10periodic"
PAM_COMMAND_PATH = "/etc/pam.d/common-passwd"
PAM_AUTH_PATH = "/etc/pam.d/common-auth"

BACKUP_PERSONAL_FILES = open("media.log","w") #"media.log"
BACKUP_DEL_USERS = open('delusers.log','w')

def check_root():
    return os.geteuid() == 0
def exec_command(command):
    try:
        result = subprocess.check_output(command,shell=True,text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def full_upgrade():
    exec_command("sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade")
    print("Updated the system, setting daily updates and security updates as well!")
    if (path.exists(UPDATE_PACKAGE_LIST_PATH)):
        exec_command("sed -i -e 's/APT::Periodic::Update-Package-Lists.*\+/APT::Periodic::Update-Package-Lists \"1\";/' /etc/apt/apt.conf.d/10periodic")
        exec_command("sed -i -e 's/APT::Periodic::Download-Upgradeable-Packages.*\+/APT::Periodic::Download-Upgradeable-Packages \"0\";/' /etc/apt/apt.conf.d/10periodic")
    if (os.system("cat /etc/apt/sources.list | grep 'deb http://security.ubuntu.com/ubuntu/ trusty-security universe main multiverse restricted'") == 1):
        exec_command("echo 'deb http://security.ubuntu.com/ubuntu/ trusty-security universe main multiverse restricted' >> /etc/apt/sources.list")
    print("System has been fully updated!")

def get_users():
    return exec_command("cat /etc/passwd | grep '/home/' | awk -F':' '{ print $1}'").strip().replace(" ","").split("\n")
def get_adm_group():
    return exec_command("cat /etc/group | grep 'adm' | awk -F ':' '{ print $4 } '").strip().split(",")

def remove_unwanted_admins():
    
    list_of_adms = get_adm_group()

    cyberpatriot_list_of_adms = ["kali"]

    for adm in list_of_adms:
        if (adm not in cyberpatriot_list_of_adms):
            print(f"Found non-listed adm account, {adm} has been spotted!")
            exec_command(f"sudo gpasswd -d {adm} adm")

def remove_media():
    MAIN_DIR = "/home"
    # i wont del any pics a they may be needed!
    ext = ["mov","mp3","mp4","wav"]

    for user in get_users():
        user = user.strip()
        if (user == " "):
            pass
        for extension in ext:
            files = glob(f"{MAIN_DIR}/{user}/*.{extension}",recursive=True)
            #print(files)
            for file in files:
                BACKUP_PERSONAL_FILES.writelines(file)
    
    BACKUP_PERSONAL_FILES.close()

    print("Possible media found, check 'media.log' for all media that needs to be remove!")

def purge_malware():
    exec_command("sudo apt purge nmap hydra ophcrack wireshark* -y")
    print("Removed unessary packages and possible 'hacking tools', please check the readme and this may not be all!")

def configure_display_manager():
    if (path.exists(LIGHT_DM_PATH)):
        exec_command(f"echo 'allow-guest=false' >> {LIGHT_DM_PATH} && systemctl restart lightdm.service") 
        print("Configured 'lightdm', disabled guest access!\nRestarting 'lightdm.server' now, screen may blackout.")

def disable_root_nologin():
    exec_command("sudo usermod -s /usr/sbin/nologin root")
    print("Disabled root login, changed shell to nologin")

def secure_sshd():
    if (path.exists(SSHD_PATH)):
        exec_command("sed -i 's/LoginGraceTime .*/LoginGraceTime 60/g' /etc/ssh/sshd_config")
        exec_command("sed -i 's/PermitRootLogin .*/PermitRootLogin no/g' /etc/ssh/sshd_config")
        exec_command("sed -i 's/Protocol .*/Protocol 2/g' /etc/ssh/sshd_config")
        exec_command("sed -i 's/#PermitEmptyPasswords .*/PermitEmptyPasswords no/g' /etc/ssh/sshd_config")
        exec_command("sed -i 's/PasswordAuthentication .*/PasswordAuthentication yes/g' /etc/ssh/sshd_config")
        exec_command("sed -i 's/X11Forwarding .*/X11Forwarding no/g' /etc/ssh/sshd_config")

        print("Securing 'sshd.service', change default polices and disabled root login!")

def setup_password_pol():
    exec_command("sudo apt install libpam-cracklib")

    if (path.exists(LOGIN_DEF_PATH)):
        exec_command("sed -i.bak -e 's/PASS_MAX_DAYS\t[[:digit:]]\+/PASS_MAX_DAYS\t90/' /etc/login.defs")
        exec_command("sed -i -e 's/PASS_MIN_DAYS\t[[:digit:]]\+/PASS_MIN_DAYS\t10/' /etc/login.defs")
        exec_command("sed -i -e 's/PASS_WARN_AGE\t[[:digit:]]\+/PASS_WARN_AGE\t7/' /etc/login.defs")
    if (path.exists(PAM_COMMON_PATH)):
        exec_command("sed -i -e 's/difok=3\+/difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1/' /etc/pam.d/common-password")
    if (path.exists(PAM_AUTH_PATH)):
        exec_command("sed -i 's/auth\trequisite\t\t\tpam_deny.so\+/auth\trequired\t\t\tpam_deny.so/' /etc/pam.d/common-auth")
        exec_command("sed -i '$a auth\trequired\t\t\tpam_tally2.so deny=5 unlock_time=1800 onerr=fail' /etc/pam.d/common-auth")
    print("Installed 'libpam-cracklib', PAM and LOGIN have been configured with secure passwd polices!")

def fix_perm_locations():
    files = ["/etc/shadow","/etc/sudoers"]

    for file in files:
        if (path.exists(file)):
            exec_command(f"sudo chmod -R 640 {file}")
            print(f"Found insecure file perms on {file}, change it to 640.")


# try to parse them from the html in the cyberpatriot folder
def find_unwanted_users():
    list_of_users = get_users()

    cyberpatriot_list_of_users = ["kali"]

    for user in list_of_users:
        
        if (user == " "):
            pass

        if (user not in cyberpatriot_list_of_users):
            print(f"Found non-listed user, {user} is not in readme.")
            exec_command(f"sudo userdel {user}")
            #print(f"{user} has been deleted")
            BACKUP_DEL_USERS.writelines(user)

    BACKUP_DEL_USERS.close()

    print("Deleted all users that could be found, check 'delusers.log' to verify!")

def secure_network():
    
    exec_command("sudo apt install ufw && sudo ufw enable")

    commands = ["sudo sysctl -n net.ipv4.tcp_syncookies","echo 'net.ipv6.conf.all.disable_ipv6 = 1' | sudo tee -a /etc/sysctl.conf","echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward","sudo echo 'net.ipv4.icmp_echo_ignore_all = 1' >> /etc/sysctl.conf"]

    for command in commands:
        exec_command(command)

    exec_command("sudo sysctl -p")
    exec_command("sudo sysctl --system")

    print("Secured networking and install/setup the firewall!")

def run_extern_program():

    ask = input("Would you also like to run another external program from github (y/n): ")

    if (ask.lower() == "y"):
        exec_command("curl https://raw.githubusercontent.com/ponkio/CyberPatriot/refs/heads/master/Linux_Ubuntu.sh | sh")

def main():
    full_upgrade()
    #purge_malware()
    disable_root_nologin()
    secure_sshd()
    secure_network()
    remove_media()
    find_unwanted_users()
    fix_perm_locations()
    remove_unwanted_admins()



    # if really needed, please go over the script before you run it!
    run_extern_program()

if __name__ == "__main__":
    if (check_root() != True):
        print("Please try again, make sure to run this script with 'root' perms.")
        exit(1)
    main()
