## Installation

First, clone this repository:

<!-- start:code block -->
# Clone this repository
git clone https://github.com/crowdsnullpointer/CyberPatriot.git

cd CyberPatriot

# Execute program
sudo python3 Debain.py
<!-- end:code block -->

<!-- start:code block -->
Find insecure functions in c

#include <stdio.h>

int main() {
char str[100];

printf("Enter a string: ");
gets(str);

printf("You entered: %s\n", str);

return 0;
}

Take a look at the 'str' variable, its buffer size is 100 bytes long.
The program takes in user input by using the 'gets' function, if you dont know any functions just look them up.

This is an issue, the 'gets' function does not ask for a length for its function or check if its longer than its buffer size, this means that the user can provide an input that is over the limit of the buffer size.
This is called a buffer-overflow, its when a given about of data from a user exceeds the size of its buffer.
So 'gets' function is insecure and should not be used.
This applys to alot of other functions that are still used today.
You could look tons of insecure functions in c libraries to figure out what is being used in the program.
<!-- start:code block -->

# Main focus
> This program really focues on any debain-based distros like ubuntu. This script is not focused on securing server services like 'mysql'. All though 'ssh' is configured in this it is mainly used on both systems anyway.
# ToDo
- Scrape readme (HTML) from cyberpatriot client to get users/adms -->
- Add some colors -->
- more debuging information -->

---
> Do not rely on this program as each scenario is unique to each year in any CyberPatriot competion, this is more of a start to automate commands as possible.

— CrowdstrikesNullPointer
