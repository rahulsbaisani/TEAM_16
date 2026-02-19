#include <stdio.h>
#include <string.h>

// Define a structure (like tuple)
struct Student {
    int id;
    float marks;
    char name[50];
};

int main() {

    // Create variable of struct
    struct Student s1;

    // Assign values
    s1.id = 101;
    s1.marks = 89.5;
    strcpy(s1.name, "Rahul");

    // Print values
    printf("ID: %d\n", s1.id);
    printf("Marks: %.2f\n", s1.marks);
    printf("Name: %s\n", s1.name);

    return 0;
}
