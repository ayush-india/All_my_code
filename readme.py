ITS ALL THE COMMANDS REQUIRE FOR NVIM-TREE AND ITS REALLY HELP FULL

|Mappings|                                       *nvim-tree-mappings*

- type `g?` to see the help UI with keybindings
- move around like in any vim buffer
- '<CR>' on '..' will cd in the above directory
- typing '<C-]>' will cd in the directory under the cursor
- typing '<BS>' will close current opened directory or parent
- typing 'P' will move cursor to the parent directory

- type 'a' to add a file
- type 'r' to rename a file
- type `<C-r>` to rename a file and omit the filename on input
- type 'x' to add/remove file/directory to cut clipboard
- type 'c' to add/remove file/directory to copy clipboard
- type 'p' to paste from clipboard. Cut clipboard has precedence over copy
  (will prompt for confirmation)
- type 'd' to delete a file (will prompt for confirmation)
- type ']c' to go to next git item
- type '[c' to go to prev git item
- type '-' to navigate up one directory
- type 's' to open a file with default system application or a folder with default file manager
- type '<' to navigate to the previous sibling of current file/directory
- type '>' to navigate to the next sibling of current file/directory
- type 'J' to navigate to the first sibling of current file/directory
- type 'K' to navigate to the last sibling of current file/directory

- if the file is a directory, '<CR>' will open the directory
- otherwise it will open the file in the buffer near the tree
- if the file is a symlink, '<CR>' will follow the symlink
- '<C-v>' will open the file in a vertical split
- '<C-x>' will open the file in a horizontal split
- '<C-t>' will open the file in a new tab
- '<Tab>' will open the file as a preview (keeps the cursor in the tree)
- 'I' will toggle visibility of folders hidden via |g:nvim_tree_ignore|
- 'R' will refresh the tree

- Double left click acts like '<CR>'
- Double right click acts like '<C-]>'

