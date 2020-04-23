create table boards(
    rounds_played integer,
    board_name text,

    constraint fk_board_owner
        foreign key (board_owner)
        REFERENCES users (id)
)


create table history(
    boards_included integer[],
    winner integer,

)


create table users(
    username varchar,
)