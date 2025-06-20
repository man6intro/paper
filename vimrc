let mapleader=" "

" {{{ plugin
call plug#begin()
" List your plugins here
Plug 'tpope/vim-sensible'
Plug 'tpope/vim-commentary'
Plug 'tpope/vim-repeat'
Plug 'tpope/vim-sleuth'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-unimpaired'
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-eunuch'
Plug 'tpope/vim-abolish'
Plug 'junegunn/seoul256.vim'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'junegunn/limelight.vim'
Plug 'junegunn/goyo.vim'
Plug 'junegunn/vim-easy-align'
Plug 'junegunn/rainbow_parentheses.vim'
Plug 'junegunn/vim-peekaboo'
Plug 'airblade/vim-gitgutter'
Plug 'mbbill/undotree'
Plug 'skywind3000/asyncrun.vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
call plug#end()

"{{{ junegunn
let g:seoul256_background = 233
let g:seoul256_light_background = 256
colo seoul256

autocmd! User GoyoEnter Limelight
autocmd! User GoyoLeave Limelight!

nmap <leader>g :Goyo<cr>

nmap <leader>f :FZF<cr>
nmap <leader>b :Buffers <cr>
nmap <leader>r :Rg<cr>
nmap <leader>l :Lines<cr>
nmap <leader>c :Changes<cr>
nmap <leader>m :Marks<cr>
nmap <leader>j :Jumps<cr>
nmap <leader>w :Windows<cr>
nmap <leader>h :History<cr>

xmap ga <Plug>(EasyAlign)
nmap ga <Plug>(EasyAlign)
"}}}

"{{{ gitgutter
set updatetime=100
command! Gqf GitGutterQuickFix | copen
nmap ]h <Plug>(GitGutterNextHunk)
nmap [h <Plug>(GitGutterPrevHunk)
"}}}

"{{{ undotree
if has("persistent_undo")
	let target_path = expand('~/.vim/undodir')
	" create the directory and any parent directories
	" if the location does not exist.
	if !isdirectory(target_path)
		call mkdir(target_path, "p", 0700)
	endif
	let &undodir=target_path
	set undofile
endif
nnoremap <leader>u :UndotreeToggle<CR>
"}}}

"{{{ airline
let g:airline#extensions#tabline#enabled = 1
let g:airline_powerline_fonts = 1
" }}}
" }}}

" {{{ set
if !has('gui_running') && &t_Co >= 256
	set termguicolors
end

if exists('filetype')
	filetype plugin indent on
endif

if has('syntax') && !exists('g:syntax_on')
	syntax on
endif

" {{{ beep
set noerrorbells
set novisualbell
set belloff=all
set t_vb=
" }}}

set number
set laststatus=2
set scrolloff=3
set sidescrolloff=3
set ttyfast
set lazyredraw
set splitright
set splitbelow
set foldmethod=marker

set ignorecase
set autoread
" set nomodeline
set modeline
set nowrap
set formatoptions+=jc
set virtualedit+=block
" }}}

" {{{ keymap
nmap <leader>. :e.<cr>
nnoremap ; :
inoremap jj <esc>
vnoremap > >gv
vnoremap < <gv
nnoremap <silent> <c-s> :w<cr>
nnoremap <silent> <c-q> :try \| tabclose \| catch \| qa \| endtry<cr>
nnoremap n nzz
" }}}
