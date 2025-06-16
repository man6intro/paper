# Set up the prompt

# autoload -Uz promptinit
# promptinit
# prompt adam1

setopt histignorealldups sharehistory

# Use emacs keybindings even if our EDITOR is set to vi
bindkey -e

# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:
HISTSIZE=100000
SAVEHIST=100000
HISTFILE=~/.zsh_history

# Use modern completion system
autoload -Uz compinit
compinit

zstyle ':completion:*' auto-description 'specify: %d'
zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' menu select=2
eval "$(dircolors -b)"
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' menu select=long
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true

zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
    zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'

# manually added !

typeset -U path PATH
# append
# path+=('/home/foo/bin')
# or prepend
# path=('/home/foo/bin' $path)
path+=(~/bin ~/.local/bin)
export PATH

export EDITOR=vim
export VISUAL=vim

export _JAVA_AWT_WM_NONREPARENTING=1

WORDCHARS='_-' # Don't consider certain characters part of the word
# hide EOL sign ('%')
PROMPT_EOL_MARK=""

setopt autocd
#setopt correct            # auto correct mistakes
setopt interactivecomments # allow comments in interactive mode
setopt magicequalsubst     # enable filename expansion for arguments of the form ‘anything=expression’
setopt nonomatch           # hide error message if there is no match for the pattern
setopt notify              # report the status of background jobs immediately
setopt numericglobsort     # sort filenames numerically when it makes sense
setopt promptsubst         # enable command substitution in prompt
setopt complete_in_word    # Complete from both ends of a word.
setopt extended_glob       # Use extended globbing syntax.
setopt auto_menu           # Show completion menu on a successive tab press.
setopt auto_list           # Automatically list choices on ambiguous completion.
unsetopt flow_control      # Redundant with tmux
unsetopt menu_complete     # Do not autoselect the first completion entry.
unsetopt complete_aliases  # Disabling this enables completion for aliases

# History configurations
setopt hist_expire_dups_first # delete duplicates first when HISTFILE size exceeds HISTSIZE
setopt hist_ignore_dups       # ignore duplicated commands history list
setopt hist_ignore_space      # ignore commands that start with space
setopt hist_verify            # show command with history expansion to user before running it
setopt share_history         # share command history data
alias history="history 0"

# zsh-users/zsh-syntax-highlighting#295
zstyle ':bracketed-paste-magic' active-widgets '.self-*'
# Don't complete unavailable commands.
zstyle ':completion:*:(functions|parameters)' ignored-patterns '(_*|.*|-*|+*|autosuggest-*|pre(cmd|exec))'

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto --group-directories-first'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -l'
alias lla='ls -la'
alias la='ls -A'
alias l='ls -CF'

# Verbosity and settings that you pretty much just always are going to want.
alias \
    cp="cp -iv" \
    mv="mv -iv" \
    rm="rm -vI" \
    bc="bc -ql" \
    rsync="rsync -vrPlu" \
    mkdir="mkdir -pv" \
    ffmpeg="ffmpeg -hide_banner" # hide build flags

# Colorize commands when possible.
alias \
    ip="ip -color=auto"\
    ports='netstat -tulanp'


# These common commands are just too long! Abbreviate them.
alias \
    ka="killall" \
    e='$EDITOR' \
    g="git"

alias bctl='bluetoothctl' \
    jc='journalctl -xe' \
    jcu='journalctl -xe -u' \
    sc=systemctl \
    scu='systemctl --user' \
    scur='systemctl --user restart' \
    scus='systemctl --user status' \
    ssc='sudo systemctl' \
    sscr='sudo systemctl restart' \
    sscs='sudo systemctl status' \
    nctl='sudo networkctl' \
    rctl='sudo resolvectl' \
    sueh='sudo -EH' \
    sue='sudo -E' \
    logpackage="dnf repoquery --userinstalled"\
    sefd='setfont -d' \
    sefontdebian='setfont /usr/share/consolefonts/Lat15-Terminus32x16.psf.gz'

if (( $+commands[udisksctl] )); then
    alias ud='udisksctl'
    alias udm='udisksctl mount -b'
    alias udu='udisksctl unmount -b'
fi

if (( $+commands[nix] )); then
    alias n=nix
    alias ne=nix-env
    alias nf='nix flake'
    alias nfm='nix flake metadata'
    alias nfs='nix flake show'
    alias nr='nix repl'
    alias nrp='nix repl "<nixpkgs>"'
    alias ns='nix shell'
    alias nsgc='nix-store --gc'
fi

if (( $+commands[xdg-open] )); then
    alias open=xdg-open
fi

# stuffs
list_ips() {
    ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "[\033[96m" iface"\033[0m] "a[1] }'
}

mkcd() {
    mkdir $1 && cd $_
}

iscmd() {
    command -v "$1" > /dev/null
}

installnix(){
    sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon
}

# {{{ plugins

# enable command-not-found if installed
if [ -f /etc/zsh_command_not_found ]; then
    . /etc/zsh_command_not_found
fi

if iscmd fzf; then
    eval "$(fzf --zsh)"
fi

if iscmd zoxide; then
    eval "$(zoxide init zsh)"
    alias cd=z
fi

if iscmd starship; then
    eval "$(starship init zsh)"
fi

install_zinit(){
    bash -c "$(curl --fail --show-error --silent --location https://raw.githubusercontent.com/zdharma-continuum/zinit/HEAD/scripts/install.sh)"
}

installzoxide(){
    curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | BIN_DIR=~/.local/bin sh
}

installstarship(){
    curl -sS https://starship.rs/install.sh | BIN_DIR=~/.local/bin sh
}

### Added by Zinit's installer
if [[ ! -f $HOME/.local/share/zinit/zinit.git/zinit.zsh ]]; then
    print -P "%F{33} %F{220}Installing %F{33}ZDHARMA-CONTINUUM%F{220} Initiative Plugin Manager (%F{33}zdharma-continuum/zinit%F{220})…%f"
    command mkdir -p "$HOME/.local/share/zinit" && command chmod g-rwX "$HOME/.local/share/zinit"
    command git clone https://github.com/zdharma-continuum/zinit "$HOME/.local/share/zinit/zinit.git" && \
        print -P "%F{33} %F{34}Installation successful.%f%b" || \
        print -P "%F{160} The clone has failed.%f%b"
fi

source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# Load a few important annexes, without Turbo
# (this is currently required for annexes)
zinit light-mode for \
    zdharma-continuum/zinit-annex-as-monitor \
    zdharma-continuum/zinit-annex-bin-gem-node \
    zdharma-continuum/zinit-annex-patch-dl \
    zdharma-continuum/zinit-annex-rust

### End of Zinit's installer chunk

zinit load zdharma-continuum/history-search-multi-word
# zinit light zsh-users/zsh-syntax-highlighting
zinit light zdharma-continuum/fast-syntax-highlighting
zinit light zsh-users/zsh-autosuggestions

# }}}
