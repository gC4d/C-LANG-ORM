#ifndef DATABASE_H
#define DATABASE_H

typedef struct Database{
   sqlite3 *db;
   char *err_msg; 
} Database;

typedef struct {
    const char* field_name;     // Field name
    const char* field_type;     // Field type
    size_t offset;              // Offset in the struct
    int is_not_null;            // 0 = nullable, 1 = not nullable
    int is_primary_key;         // 1 = primary key, 0 = not primary key
} FieldDescriptor;

typedef struct {                
    const char* table_name;    // Table name
    FieldDescriptor* fields;   // List of fields in the table  
    int field_count;           // Count of fields in the table
} TableDescriptor;

Database* db_init(const char *db_name);
void serialize_to_sql(const TableDescriptor* table, const void* object, char* sql_buffer);
void db_select(const TableDescriptor* table, void* object, const char** row_data);
void db_insert(); // ToDo
void db_update(); // ToDo
void db_delete(); // ToDo

#endif