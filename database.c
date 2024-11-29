#include<stdio.h>
#include<stdlib.h>
#include<sqlite3.h> 
#include "database.h"

Database* db_init(const char *db_name) {
    Database *database = malloc(sizeof(Database));
    if (!database) {
        fprintf(stderr, "Memory allocation failed!\n");
        return NULL;
    }

    int rc = sqlite3_open(db_name, &database->db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(database->db));
        free(database);
        return NULL;
    }

    database->err_msg = NULL;
    return database;
}