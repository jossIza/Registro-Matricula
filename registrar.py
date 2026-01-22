import streamlit as st
import pandas as pd 
import streamlit.components.v1 as components


asignaturas={
    "Programacion en la nube":{"catedratico":"Ing- Elvin Mackdonalds", "aula":"A-100"},
    "Sistemas Operativos l":{"catedratico":"Ing- Marlon Perez", "aula":"A-101"},
    "Programacion Estructurada":{"catedratico":"Ing- Joel Sauceda", "aula":"A-102"},
    "Programacion Web l":{"catedratico":"Ing- Isaias Deras", "aula":"A-103"},
    "Matematicas l":{"catedratico":"Lic- Donald Dimas", "aula":"A-104"},
    "Español":{"catedratico":"Master- Maynor Hernandez", "aula":"A-105"}
}

horaIncioClase={"07:00","08:10","10:10","14:00", "13:00","14:10", "15:10"}
horaFinalizaClase={"07:50", "10:00", "11:10", "14:10","15:00", "16:00"}


if "tablaMatricula" not in st.session_state:
    st.session_state.tablaMatricula = pd.DataFrame(
        columns=["Nombre", "DNI", "Asignatura", "HoraInicio", "HoraFinaliza", "Catedratico", "Aula"]
    )

st.title("REGISTRO DE ESTUDIANTES CEB, JUAN LIND0")

with st.form("formularioMatricula", clear_on_submit=True):
    st.subheader("Ingreso de los datos del estudiante")

    col1, col2= st.columns(2)
    nombre= col1.text_input("Nombre Completo del estudiante", key="nombreInput")
    dni= col2.text_input("Identidad-(DNI)")

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4= st.columns(2)
    telefono= col3.text_input("Celular/ Padre del estudiante")
    Domicilio= col4.text_input("Lugar de residencia --Aldea, punto de refrencia")

    st.divider()

    st.subheader("Selecciona la clase que vas a matricular")

    claseSeleccionada= st.selectbox("Area de seleccion de asignaturas a matricular", list(asignaturas.keys()))

    c1, c2= st.columns(2)
    horaInicioElegida= c1.selectbox("Selecciona la hora que quieres que inicie la clase", horaIncioClase)
    horaFinalizaElegida= c2.selectbox("Selecciona la hora que quieres que finalice la clase", horaFinalizaClase)
    
    btnMatricular=st.form_submit_button("Guardar Registro")

    if btnMatricular:
        if nombre and dni:
            datosClaseSeleccionada= asignaturas[claseSeleccionada]

            nueva_clase={
                "Nombre": nombre,
                "DNI": dni,
                "Asignatura": claseSeleccionada,
                "HoraInicio": horaInicioElegida,
                "HoraFinaliza": horaFinalizaElegida, # Corregido para coincidir con el DataFrame
                "Catedratico": datosClaseSeleccionada["catedratico"],
                "Aula": datosClaseSeleccionada["aula"]
            }

            st.session_state.tablaMatricula=pd.concat(
                [st.session_state.tablaMatricula, pd.DataFrame([nueva_clase])],
                ignore_index=True
            )

            # Corregido: sintaxis de f-string
            st.success(f"La matrícula de la clase {claseSeleccionada} fue realizada con éxito!")

        else:
            st.error("Favor asegurese de llenar el espacio del nombre y DNI")


st.divider()
st.subheader("Cuadro de matriculas inscritas")   
st.dataframe(st.session_state.tablaMatricula, use_container_width=True)

if not st.session_state.tablaMatricula.empty:
    with st.expander("Aqui puedes borrar clases segun items "):
        opciones= st.session_state.tablaMatricula.index.tolist()
        itemSeleccionado= st.selectbox("Elije cual clase matriculada vas a eliminar", opciones)

        if st.button("Eliminar clase seleccionada"):
            st.session_state.tablaMatricula= st.session_state.tablaMatricula.drop(itemSeleccionado)
            st.session_state.tablaMatricula.reset_index(drop=True, inplace=True)
            st.success("clase eliminada con exito")
            st.rerun()


# --- MOSTRAR EL COMPROBANTE ---
if st.button("Generar comprobante"):
    if not st.session_state.tablaMatricula.empty:
        st.subheader("Confirmación de Matrícula")
        
        for i, fila in st.session_state.tablaMatricula.iterrows():
            with st.expander(f"Detalle: {fila['Asignatura']}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Estudiante:** {fila['Nombre']}")
                    st.write(f"**DNI:** {fila['DNI']}")
                    st.write(f"**Asignatura:** {fila['Asignatura']}")
                
                with col2:
                    st.write(f"**Horario:** {fila['HoraInicio']} - {fila['HoraFinaliza']}")
                    st.write(f"**Catedrático:** {fila['Catedratico']}")
                    st.write(f"**Aula:** {fila['Aula']}")

        st.components.v1.html("""
            <script>function printPage() { window.print(); }</script>
            <button onclick="printPage()" style="background-color: #FF4B4B; color: white; padding: 10px; border: none; border-radius: 5px; width: 100%; cursor: pointer;">
                DESCARGAR PDF / IMPRIMIR
            </button>
        """, height=70)
    else:
        st.warning("No hay clases matriculadas aún.")