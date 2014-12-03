# heibot

This is the bot that exists on EasyCTF IRC.

## Features

- Greet it, and it'll greet you back :D
- Gets stats from the EasyCTF API.

## Commands

#### <3

Usage:

    `<3

Will say `<3` back to you :)

#### flag

Usage:

    `flag [problem_name]

Sends you the flag for `problem_name` in a private message.

#### helixfossil

Usage:

    `hf [question]

Predicts the future for your question. The Helix Fossil is always accurate.

#### help

Usage:

    `help

Displays the list of commands.

#### md5

Usage:

    `md5 [string]
    
Prints the md5 hash of `string` into the chat.

#### rek

Usage:

    `rek [username]

Reks the user who's username is `username`.

#### roll

Usage:

    `roll [max]

Generates a random number and prints it to the chat. Maximum should be greater than 1. If maximum is not specified, it will default to 1000.

#### solved

Usage:

    `solved [problem_name]
    
Prints the number of teams who have successfully solved `problem_name` to the chat. Must use the exact problem name, but is case insensitive (for example, `the door` instead of `thedoor` or `door`).

#### top

Usage:

    `top [n]

Prints the status of the top `n` teams to the chat. If `n` is not specified, then it will default to 5. It prints in this format:

    [n]: [teamname], [pts]
