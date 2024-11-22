"""Blueprint del programa que muestra datos de la DB"""
from flask import (
    Blueprint, render_template, request  # , url_for, redirect
)

from app.db import get_db

bp = Blueprint('show', __name__, url_prefix='/show',
               template_folder='show/templates/show')


@bp.route('/', methods=['GET', 'POST'])
def index():
    """Home de Show"""
    if request.method == 'POST':
        return "show index POST"
    return render_template('index.html')


def datos_tabla(tabla, where=None):
    """Mostar datos de la tabla 'tabla'"""
    db, c = get_db()
    c.execute(f"SELECT * FROM {tabla} {where}")
    return c.fetchall()


@bp.route('programas', methods=['GET'])
def programas():
    """Mostar datos de la tabla programas"""
    where = "WHERE activo = 1"
    datos = datos_tabla('programas', where=where)

    # print([*datos[0]])
    return render_template('programas.html', datos=datos)


@bp.route('grupos', methods=['GET'])
def grupos():
    """Mostrar datos de la tabla grupos"""
    datos = datos_tabla('grupos')

    return render_template('grupos.html', datos=datos)


@bp.route('facturar_que', methods=['GET', 'POST'])
def facturar_que():
    """Seleccionar fecha y programas a facturar"""
    if request.method == 'POST':
        ano_mes = request.form.get('ano-mes')
        ch_id = request.form.get('id')
        ano, mes = ano_mes.split('-')

        datos = datos_facturar(ch_id, ano, mes)
        return render_template('datos_facturar.html', datos=datos)

    else:
        db, c = get_db()
        c.execute("SELECT id, nombre_monitor FROM programas WHERE activo=1")
        lista_programas = c.fetchall()
        return render_template('facturar_que.html', programas=lista_programas)


def datos_facturar(ch_id=None, ano=None, mes=None):
    """Sacar datos a facturar"""
    caso_especial = ""
    if ch_id == "17" and ano == "2022" and mes == "11":
        caso_especial = """AND llamadas.log_name <> 'tomfp'
                AND llamadas.log_name <> 'yudith' \n"""

    SELECT = f"""
        (
            SELECT YEAR(llamadas.fecha) AS Año,
            MONTH(llamadas.fecha) AS Mes,
            agentes.nombre AS Nombre, agentes.log_name AS Agente,
            programas.nombre_monitor AS Programa,
            FORMAT( programas.factura_hora , 2, 'es_ES') AS '€/día',
            COUNT(DISTINCT fecha) AS 'Núm. días',
            FORMAT ( COUNT(DISTINCT fecha) * programas.factura_hora, 2, 'es_ES') AS 'Total €'
            FROM agentes
            INNER JOIN llamadas ON llamadas.log_name = agentes.log_name
            INNER JOIN grupos ON grupos.grupo = agentes.grupo
            INNER JOIN programas ON programas.id = llamadas.programa_id
            WHERE YEAR(llamadas.fecha) = ? AND MONTH(llamadas.fecha) = ?
            AND llamadas.programa_id = ?
            {caso_especial}
            GROUP BY llamadas.log_name
            ORDER BY grupos.grupo, llamadas.log_name
        )
        UNION (
            SELECT '-----', '---', '-----', '-----',
            '-TOTAL:-->', e_hora, SUM(n_dias),
            CAST( FORMAT ( SUM(kk) , 2, 'es_ES') AS CHAR)
            FROM (
                SELECT
                FORMAT(programas.factura_hora, 2, 'es_ES') AS e_hora,
                (COUNT(DISTINCT fecha) ) AS n_dias,
                (COUNT(DISTINCT fecha) * programas.factura_hora ) AS kk
                FROM agentes
                INNER JOIN llamadas ON llamadas.log_name = agentes.log_name
                INNER JOIN grupos ON grupos.grupo = agentes.grupo
                INNER JOIN programas ON programas.id = llamadas.programa_id
                WHERE YEAR(llamadas.fecha) = ? AND MONTH(llamadas.fecha) = ?
                AND llamadas.programa_id = ?
                {caso_especial}
                GROUP BY llamadas.log_name
            ) totals_result
        )
    """
    db, c = get_db()
    c.execute(SELECT, (ano, mes, ch_id, ano, mes, ch_id))
    datos = c.fetchall()

    return datos
