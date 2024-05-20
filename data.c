#include <stdio.h>
#include <stdlib.h>
#include <sql.h>
#include <sqlext.h>
#include <string.h>

#define USERNAME_LEN 50
#define PASSWORD_LEN 50
#define PRODUCT_NAME_LEN 100

void handle_error(SQLHANDLE handle, SQLSMALLINT type, RETCODE retcode);
SQLHENV env;
SQLHDBC dbc;

void connect_to_db() {
    SQLRETURN retcode;

    SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);
    SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void *) SQL_OV_ODBC3, 0);

    SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);

    retcode = SQLDriverConnect(dbc, NULL,
        (SQLCHAR*) "DRIVER={ODBC Driver 17 for SQL Server};SERVER=<your_server>.database.windows.net;DATABASE=<your_db>;UID=<your_user>;PWD=<your_password>;",
        SQL_NTS, NULL, 0, NULL, SQL_DRIVER_COMPLETE);

    if (SQL_SUCCEEDED(retcode)) {
        printf("Connected to the database.\n");
    } else {
        handle_error(dbc, SQL_HANDLE_DBC, retcode);
        exit(1);
    }
}

void disconnect_from_db() {
    SQLDisconnect(dbc);
    SQLFreeHandle(SQL_HANDLE_DBC, dbc);
    SQLFreeHandle(SQL_HANDLE_ENV, env);
}

void handle_error(SQLHANDLE handle, SQLSMALLINT type, RETCODE retcode) {
    if (retcode == SQL_INVALID_HANDLE || retcode == SQL_ERROR) {
        SQLCHAR message[1000];
        SQLCHAR state[SQL_SQLSTATE_SIZE + 1];
        SQLINTEGER native;
        SQLSMALLINT len;
        SQLGetDiagRec(type, handle, 1, state, &native, message, sizeof(message), &len);
        printf("Error: %s, SQLSTATE: %s\n", message, state);
    }
}

// função para login
int login() {
    char username[USERNAME_LEN];
    char password[PASSWORD_LEN];
    SQLHSTMT stmt;
    SQLRETURN retcode;
    int user_id = 0;

    printf("Username: ");
    scanf("%s", username);
    printf("Password: ");
    scanf("%s", password);

    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLPrepare(stmt, (SQLCHAR*)"SELECT id FROM users WHERE username = ? AND password = ?", SQL_NTS);
    SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, username, 0, NULL);
    SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, password, 0, NULL);

    retcode = SQLExecute(stmt);

    if (SQL_SUCCEEDED(retcode)) {
        SQLBindCol(stmt, 1, SQL_C_LONG, &user_id, 0, NULL);
        if (SQLFetch(stmt) == SQL_NO_DATA) {
            printf("Login failed. Incorrect username or password.\n");
            user_id = 0;
        } else {
            printf("Login successful. User ID: %d\n", user_id);
        }
    } else {
        handle_error(stmt, SQL_HANDLE_STMT, retcode);
    }

    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
    return user_id;
}

void register_user() {
    char username[USERNAME_LEN];
    char password[PASSWORD_LEN];
    SQLHSTMT stmt;
    SQLRETURN retcode;

    printf("Username: ");
    scanf("%s", username);
    printf("Password: ");
    scanf("%s", password);

    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLPrepare(stmt, (SQLCHAR*)"INSERT INTO users (username, password) VALUES (?, ?)", SQL_NTS);
    SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, username, 0, NULL);
    SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, password, 0, NULL);

    retcode = SQLExecute(stmt);

    if (SQL_SUCCEEDED(retcode)) {
        printf("User registered successfully.\n");
    } else {
        handle_error(stmt, SQL_HANDLE_STMT, retcode);
    }

    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

void add_product() {
    char name[PRODUCT_NAME_LEN];
    double price;
    SQLHSTMT stmt;
    SQLRETURN retcode;

    printf("Product Name: ");
    scanf("%s", name);
    printf("Price: ");
    scanf("%lf", &price);

    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLPrepare(stmt, (SQLCHAR*)"INSERT INTO products (name, price) VALUES (?, ?)", SQL_NTS);
    SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, name, 0, NULL);
    SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE, 0, 0, &price, 0, NULL);

    retcode = SQLExecute(stmt);

    if (SQL_SUCCEEDED(retcode)) {
        printf("Product added successfully.\n");
    } else {
        handle_error(stmt, SQL_HANDLE_STMT, retcode);
    }

    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

void view_products() {
    SQLHSTMT stmt;
    SQLRETURN retcode;
    SQLCHAR name[PRODUCT_NAME_LEN];
    double price;

    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLExecDirect(stmt, (SQLCHAR*)"SELECT name, price FROM products", SQL_NTS);

    SQLBindCol(stmt, 1, SQL_C_CHAR, name, sizeof(name), NULL);
    SQLBindCol(stmt, 2, SQL_C_DOUBLE, &price, 0, NULL);

    while (SQLFetch(stmt) != SQL_NO_DATA) {
        printf("Product Name: %s, Price: %.2f\n", name, price);
    }

    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

// menu principal
void menu() {
    int choice;
    int user_id = 0;

    while (1) {
        printf("\nMenu:\n");
        printf("1. Login\n");
        printf("2. Register User\n");
        printf("3. Add Product\n");
        printf("4. View Products\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                user_id = login();
                break;
            case 2:
                register_user();
                break;
            case 3:
                if (user_id) {
                    add_product();
                } else {
                    printf("You need to log in first.\n");
                }
                break;
            case 4:
                view_products();
                break;
            case 5:
                disconnect_from_db();
                exit(0);
            default:
                printf("Invalid choice.\n");
        }
    }
}

int main() {
    connect_to_db();
    menu();
    return 0;
}