# -------- local testing
testing: 
	echo "------------------ devloping locally ------------------"

create_local_folders: testing
	mkdir -p postgres_data mysql_data cassandra_data

run_1: create_local_folders
	docker compose up -d





# -------- production
production: 
	echo "deploying to production"