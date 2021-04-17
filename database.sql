

-- CREATE TABLE users (
--     id VARCHAR  PRIMARY KEY,
--     name VARCHAR (50)  NOT NULL,
--     last_name VARCHAR (50) NOT NULL,
--     email VARCHAR (100) UNIQUE NOT NULL,
--     tel VARCHAR (50) UNIQUE NOT NULL,
--     user_name VARCHAR (50) UNIQUE NOT NULL, 
--     password  bytea  NOT NULL,
--     user_type VARCHAR (50)  NOT NULL

-- );





-- CREATE TABLE clients (
--     id VARCHAR  PRIMARY KEY,
--     name VARCHAR (50)  NOT NULL,
--     last_name VARCHAR (50) NOT NULL,
--     email VARCHAR (100) UNIQUE NOT NULL,
--     tel VARCHAR (50) UNIQUE NOT NULL
-- );


-- CREATE TABLE contract (
--     id VARCHAR  PRIMARY KEY,
--     creation_date DATE NOT NULL DEFAULT NOW(),
--     start_date DATE,
--     end_date DATE,
--     price  FLOAT  NOT NULL,
--     contract_type  VARCHAR(50)  NOT NULL,
--     status VARCHAR(50) NOT NULL DEFAULT 'pending',
--     client_id VARCHAR NOT NULL ,
--     FOREIGN KEY (client_id) REFERENCES clients(id)

-- );

-- CREATE TABLE address  (
--     id VARCHAR  PRIMARY KEY,
--     line1 VARCHAR(100) NOT NULL,
--     line2 VARCHAR(100),
--     city VARCHAR(50) ,
--     postal_code INTEGER,
--     STATE VARCHAR(50) NOT NULL,
--     country VARCHAR (50) NOT NULL DEFAULT 'Tunisie',
--     client_id VARCHAR NOT NULL ,
--     FOREIGN KEY (client_id) REFERENCES clients(id)

-- );

-- CREATE TABLE sinisters(
--     id serial PRIMARY KEY ,
--     DESCRIPTION  VARCHAR(200),
--     creation_date DATE NOT NULL DEFAULT NOW(),
--     status VARCHAR(50) DEFAULT'in progress',
--     closing_date DATE,
--     opposing_insurer VARCHAR(50),
--     amount FLOAT,
--     client_id VARCHAR NOT NULL,
--     FOREIGN KEY (client_id) REFERENCES clients(id)
-- );

-- CREATE TABLE indemnity(
--     id serial PRIMARY KEY,
--     sinister_id INTEGER UNIQUE,
--     amount FLOAT,
--     refund_status VARCHAR(50) DEFAULT 'Not Made',
--     client_id VARCHAR NOT NULL,
--     creation_date DATE NOT NULL DEFAULT NOW(),
--     FOREIGN KEY (client_id) REFERENCES clients(id),
--     FOREIGN KEY (sinister_id) REFERENCES sinisters(id)
-- )

-- CREATE TABLE indemnity(
--     id serial PRIMARY KEY,
--     sinister_id INTEGER UNIQUE,
--     amount FLOAT,
--     refund_status VARCHAR(50) DEFAULT 'Not Made',
--     client_id VARCHAR NOT NULL,
--     creation_date DATE NOT NULL DEFAULT NOW(),
--     FOREIGN KEY (client_id) REFERENCES clients(id),
--     FOREIGN KEY (sinister_id) REFERENCES sinisters(id)
-- )
-- drop TABLE instalments;

-- CREATE TABLE instalments(
--     id serial PRIMARY KEY,
--     due_date Date NOT NULL,
--     amount FLOAT NOT NULL,
--     Payment_mode VARCHAR(50),
--     payment_date DATE ,
--     status VARCHAR(50) default 'en attente',
--     client_id VARCHAR NOT NULL,
--     contract_id VARCHAR NOT NULL,
--     FOREIGN KEY (client_id) REFERENCES clients(id),
--     FOREIGN KEY (contract_id) REFERENCES contract(id)
-- );



-- SELECT array_agg(due_date),client_id,sum(amount) from instalments where due_date<now() group by client_id HAVING client_id='3a652064-2533-4088-8e1d-997db863dc01'


-- select  sum(instalments.amount) from instalments where  due_date>NOW() group by status ,due_date,instalments.client_id HAVING   status!='payée'and client_id='3a652064-2533-4088-8e1d-997db863dc01'
-- SELECT client_id,sum(amount) from instalments where due_date < NOW() group by client_id

-- '6b7d1c38-0895-4a7d-b334-40dc25eab0d5'


-- SELECT Distinct cl.id,name,last_name,email,tel
--         ,array_agg(con.id),array_agg(con.creation_date)
--         ,array_agg(start_date),array_agg(end_date),array_agg(price)
--         ,array_agg(contract_type),array_agg(con.status),
--         ad.id,line1,line2,city,postal_code,state,country
--         ,array_agg(sin.id),array_agg(DESCRIPTION),array_agg(sin.creation_date),
--         array_agg(sin.status),array_agg(closing_date),array_agg(opposing_insurer),array_agg(sin.amount),
--         array_agg(indem.id ),array_agg(indem.sinister_id ),array_agg(indem.amount),array_agg(indem.refund_status),array_agg(indem.creation_date)
--         ,(SELECT sum(amount) from instalments where due_date<now() group by client_id HAVING client_id='6b7d1c38-0895-4a7d-b334-40dc25eab0d5') as imp
--         from clients cl
--         left join address ad on cl.id= ad.client_id
--         left join contract con on cl.id=con.client_id
--         left join sinisters sin on cl.id=sin.client_id
--         left join indemnity indem on cl.id=indem.client_id
--         where cl.id='6b7d1c38-0895-4a7d-b334-40dc25eab0d5'
--         group by cl.id,name,last_name,email,tel,con.client_id,ad.id,country;


SELECT due_date,client_id from instalments where status='en attente' order by due_date ;
-- SELECT array_agg(status),array_agg(due_date),client_id,sum(amount) from instalments  where status !='payé'and due_date<NOW() GROUP by client_id ;