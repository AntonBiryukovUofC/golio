create table users(
    id integer primary key,
    username varchar,
    email varchar
);


create table boards(
    id integer primary key,
    board_elo integer,
    board integer[],
    width integer,
    board_owner integer,
    constraint fk_board_owner
        foreign key (board_owner)
        REFERENCES users (id)
);


create table history(
    id integer primary key,
    boards_included integer[],
    winner integer
);
