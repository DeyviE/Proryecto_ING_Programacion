from servicios.agregar_libro import AgregarLibro
from servicios.agregar_usuario import AgregarUsuario
from servicios.listar_libros import ListarLibros
from servicios.listar_usuarios import ListarUsuarios
from servicios.prestar_libro import PrestarLibro
from servicios.listar_libros_prestados import ListarLibrosPrestados
from servicios.devolver_libro import DevolverLibro

def menu():
    while True:
        print("\n=== Menú del Sistema de Biblioteca ===")
        print("1. Agregar libro")
        print("2. Agregar usuario")
        print("3. Listar libros")
        print("4. Listar usuarios")
        print("5. Prestar libro")
        print("6. Listar libros prestados")
        print("7. Devolver libro")
        print("8. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            titulo = input("Título: ")
            autor  = input("Autor: ")
            isbn   = input("ISBN: ")
            AgregarLibro().ejecutar(titulo, autor, isbn)

        elif opcion == '2':
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            AgregarUsuario().ejecutar(nombre, correo)

        elif opcion == '3':
            ListarLibros().ejecutar()

        elif opcion == '4':
            ListarUsuarios().ejecutar()

        elif opcion == '5':
            libro_id   = int(input("ID del libro: "))
            usuario_id = int(input("ID del usuario: "))
            PrestarLibro().ejecutar(libro_id, usuario_id)

        elif opcion == '6':
            ListarLibrosPrestados().ejecutar()

        elif opcion == '7':
            libro_id = int(input("ID del libro a devolver: "))
            DevolverLibro().ejecutar(libro_id)

        elif opcion == '8':
            print("Gracias por usar el sistema.")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
