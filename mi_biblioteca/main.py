from servicios.agregar_libro import AgregarLibro
from servicios.agregar_usuario import AgregarUsuario
from servicios.listar_libros import ListarLibros
from servicios.listar_usuarios import ListarUsuarios
from servicios.prestar_libro import PrestarLibro
from servicios.listar_libros_prestados import ListarLibrosPrestados
from servicios.devolver_libro import DevolverLibro
from modelos.GestionBiblioteca import GestionBiblioteca
from modelos.GestionBiblioteca import GestionBiblioteca


gestion = GestionBiblioteca()

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
        print("9. Motrar actividad de un usuario")
        print("12. Modificar información de un usuario")
        print("13. Modificar información de un libro")
        print("14. Modificar un préstamo")
        print("20. Salir")

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
            PrestarLibro(gestion).ejecutar(libro_id, usuario_id)


        elif opcion == '6':
            ListarLibrosPrestados().ejecutar()

        elif opcion == '7':
            libro_id = int(input("ID del libro a devolver: "))
            DevolverLibro().ejecutar(libro_id)
        elif opcion == '9':
            usuario_id = int(input("ID del usuario: "))
            ActividadUsuario().ejecutar(usuario_id)
        
        elif opcion == '12':
            usuario_id = int(input("ID del usuario a modificar: "))
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_correo = input("Nuevo correo: ")
            ModificarUsuario().ejecutar(usuario_id, nuevo_nombre, nuevo_correo)

        elif opcion == '13':
            libro_id = int(input("ID del libro a modificar: "))
            nuevo_titulo = input("Nuevo título: ")
            nuevo_autor = input("Nuevo autor: ")
            nuevo_isbn = input("Nuevo ISBN: ")
            ModificarLibro().ejecutar(libro_id, nuevo_titulo, nuevo_autor, nuevo_isbn)

        elif opcion == '14':
            prestamo_id = int(input("ID del préstamo a modificar: "))
            nuevo_libro_id = int(input("Nuevo ID de libro: "))
            nuevo_usuario_id = int(input("Nuevo ID de usuario: "))
            nueva_fecha_prestamo = input("Nueva fecha de préstamo (YYYY-MM-DD): ")
            devolver = input("¿Ya se devolvió el libro? (s/n): ").strip().lower()
            if devolver == 's':
                nueva_fecha_devolucion = input("Fecha de devolución (YYYY-MM-DD): ")
            else:
                nueva_fecha_devolucion = None
            ModificarPrestamo().ejecutar(prestamo_id, nuevo_libro_id, nuevo_usuario_id, nueva_fecha_prestamo, nueva_fecha_devolucion)


        elif opcion == '20':
            print("Gracias por usar el sistema.")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
