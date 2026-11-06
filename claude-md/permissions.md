## Safety nets

- **Never kill programs by a loose name** (`pkill -f node`). Find the process and stop it by its
  number; the `block-broad-kill` hook stops kills that would hit other running programs.
