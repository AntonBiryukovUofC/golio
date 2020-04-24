create table users(
    username varchar primary key
);


create table boards(
    id SERIAL primary key,
    board_elo integer,
    board json,
    board_owner varchar,
    board_name varchar,
    constraint fk_board_owner
        foreign key (board_owner)
        REFERENCES users (username)
);


create table history(
    id SERIAL primary key,
    boards_included integer[],
    winner integer
);

insert into users (username, email) VALUES ('brayden', 'brayden.arthur@energytoolbase.com');