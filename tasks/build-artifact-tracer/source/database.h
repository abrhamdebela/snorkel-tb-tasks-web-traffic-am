#ifndef DATABASE_H
#define DATABASE_H

int initialize_database(void);
void cleanup_database(void);
int execute_query(const char *query);
int insert_record(const char *table, const char *data);

#endif
