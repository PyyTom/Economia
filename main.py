import sqlite3,datetime,locale,shutil,os
locale.setlocale(locale.LC_ALL, 'es_ES')
if os.path.isdir('ECONOMIA') == False:os.mkdir('ECONOMIA')
db = sqlite3.connect('ECONOMIA/' + str(datetime.datetime.today().year) + '.db')
db.execute('create table if not exists ECONOMIA(ACCION,MES integer,DIA integer,DESCRIPCION,SUMA float)')
db.close()
meses={1:['ENERO',31],2:['FEBRERO',28],3:['MARZO',31],4:['ABRIL',30],5:['MAYO',31],6:['JUÑO',30],7:['JULIO',31],8:['AGOSTO',31],9:['SEPTIEMBRE',30],10:['OCTUBRE',31],11:['NOVIEMBRE',30],12:['DICIEMBRE',31]}
from flet import *
def main(page: Page):
    def muestra_año(e):
        dd_mes.disabled, dd_dia.disabled = (False, True)
        dd_mes.value, dd_dia.value = ('', '')
        db = sqlite3.connect('ECONOMIA/' + dd_año.value + '.db')
        if db.execute('select sum(SUMA) from ECONOMIA where ACCION="INGRESO"').fetchone()[0] is not None:
            c_ingresos.controls = [Row([Text(dd_año.value + ' TOT. €.' + str(round(db.execute('select sum(SUMA) from ECONOMIA where ACCION="INGRESO"').fetchone()[0],2)), size=30)], alignment=MainAxisAlignment.CENTER)]
            c_ingresos.controls.append(Row([Text('DIA', size=20, width=100), Text('MES', size=20, width=100), Text('DESCRIPCION', size=20, width=200), Text('SUMA', size=20, width=100)], alignment=MainAxisAlignment.CENTER))
            for ingreso in db.execute('select * from ECONOMIA where ACCION="INGRESO" order by MES,DIA').fetchall():
                n_dia = str(datetime.datetime(int(dd_año.value),int(ingreso[1]), int(ingreso[2])).strftime('%A'))
                c_ingresos.controls.append(Container(content=Row([Text(n_dia, width=70), Text(ingreso[2], width=30), Text(meses[ingreso[1]][0], width=200), Text(ingreso[3], width=200), Text(ingreso[4], width=100)], alignment=MainAxisAlignment.CENTER), on_click=borra, bgcolor=colors.GREEN_50))
        else:  # inserted
            c_ingresos.controls = [Row([Text(dd_año.value + ' TOT. €.0', size=30)], alignment=MainAxisAlignment.CENTER)]
        if db.execute('select sum(SUMA) from ECONOMIA where ACCION="GASTO"').fetchone()[0] is not None:
            c_gastos.controls = [Row([Text(dd_año.value + ' TOT. €.' + str(round(db.execute('select sum(SUMA) from ECONOMIA where ACCION="GASTO"').fetchone()[0],2)), size=30)], alignment=MainAxisAlignment.CENTER)]
            c_gastos.controls.append(Row([Text('DIA', size=20, width=100), Text('MES', size=20, width=100), Text('DESCRIPCION', size=20, width=200), Text('SUMA', size=20, width=100)], alignment=MainAxisAlignment.CENTER))
            for gasto in db.execute('select * from ECONOMIA where ACCION="GASTO" order by MES,DIA').fetchall():
                n_dia = str(datetime.datetime(int(dd_año.value), int(gasto[1]), int(gasto[2])).strftime('%A'))
                c_gastos.controls.append(Container(content=Row([Text(n_dia, width=70), Text(gasto[2], width=30), Text(meses[gasto[1]][0], width=200), Text(gasto[3], width=200), Text(gasto[4], width=100)], alignment=MainAxisAlignment.CENTER), on_click=borra, bgcolor=colors.AMBER_50))
        else:c_gastos.controls = [Row([Text(dd_año.value + ' TOT. €.0', size=30)], alignment=MainAxisAlignment.CENTER)]
        db.close()
        page.update()
    def muestra_mes(e):
        dd_dia.disabled = False
        dd_dia.value = ''
        dd_dia.options = [dropdown.Option(d) for d in range(1, meses[datetime.datetime.strptime(dd_mes.value,'%B').month][1] + 1)]
        db = sqlite3.connect('ECONOMIA/' + dd_año.value + '.db')
        if db.execute('select sum(SUMA) from ECONOMIA where ACCION="INGRESO" and MES=?', (datetime.datetime.strptime(dd_mes.value,'%B').month,)).fetchone()[0] is not None:
            c_ingresos.controls = [Row([Text(dd_mes.value + ' ' + dd_año.value + ' TOT. €.' + str(round(db.execute('select sum(SUMA) from ECONOMIA where ACCION="INGRESO" and MES=?', (datetime.datetime.strptime(dd_mes.value,'%B').month,)).fetchone()[0],2)), size=30)], alignment=MainAxisAlignment.CENTER)]
            c_ingresos.controls.append(Row([Text('DIA', size=20, width=100), Text('DESCRIPCION', size=20, width=200), Text('SUMA', size=20, width=100)], alignment=MainAxisAlignment.CENTER))
            for ingreso in db.execute('select * from ECONOMIA where ACCION="INGRESO" and MES=? order by DIA', (datetime.datetime.strptime(dd_mes.value,'%B').month,)).fetchall():
                n_dia = str(datetime.datetime(int(dd_año.value),datetime.datetime.strptime(dd_mes.value,'%B').month, int(ingreso[2])).strftime('%A'))
                c_ingresos.controls.append(Container(content=Row([Text(n_dia, width=70), Text(ingreso[2], width=30), Text(ingreso[3], width=200), Text(ingreso[4], width=200)], alignment=MainAxisAlignment.CENTER), on_click=borra, bgcolor=colors.GREEN_50))
        else:c_ingresos.controls = [Row([Text(dd_mes.value + ' ' + dd_año.value + ' TOT. €.0', size=30)], alignment=MainAxisAlignment.CENTER)]
        if db.execute('select sum(SUMA) from ECONOMIA where ACCION="GASTO" and MES=?', (datetime.datetime.strptime(dd_mes.value,'%B').month,)).fetchone()[0] is not None:
            c_gastos.controls = [Row([Text(dd_mes.value + ' ' + dd_año.value + ' TOT. €.' + str(round(db.execute('select sum(SUMA) from ECONOMIA where ACCION="GASTO" and MES=?', (datetime.datetime.strptime(dd_mes.value,'%B').month,)).fetchone()[0],2)), size=30)], alignment=MainAxisAlignment.CENTER)]
            c_gastos.controls.append(Row([Text('DIA', size=20, width=100), Text('DESCRIPCION', size=20, width=200), Text('SUMA', size=20, width=100)], alignment=MainAxisAlignment.CENTER))
            for gasto in db.execute('select * from ECONOMIA where ACCION="GASTO" and MES=? order by DIA', (datetime.datetime.strptime(dd_mes.value,'%B').month,)).fetchall():
                n_dia = str(datetime.datetime(int(dd_año.value),datetime.datetime.strptime(dd_mes.value,'%B').month, int(gasto[2])).strftime('%A'))
                c_gastos.controls.append(Container(content=Row([Text(n_dia, width=70), Text(gasto[2], width=30), Text(gasto[3], width=200), Text(gasto[4], width=200)], alignment=MainAxisAlignment.CENTER), on_click=borra, bgcolor=colors.AMBER_50))
        else:c_gastos.controls = [Row([Text(dd_mes.value + ' ' + dd_año.value + ' TOT. €.0', size=30)], alignment=MainAxisAlignment.CENTER)]
        db.close()
        page.update()
    def muestra_dia(e):
        db = sqlite3.connect('ECONOMIA/' + dd_año.value + '.db')
        if db.execute('select sum(SUMA) from ECONOMIA where ACCION="INGRESO" and MES=? and DIA=?', (datetime.datetime.strptime(dd_mes.value,'%B').month, dd_dia.value)).fetchone()[0] is not None:
            c_ingresos.controls = [Row([Text(str(datetime.datetime(int(dd_año.value),datetime.datetime.strptime(dd_mes.value,'%B').month, int(dd_dia.value)).strftime('%A')) + ' ' + dd_dia.value + ' ' + dd_mes.value+ ' ' + dd_año.value + ' TOT. €.' + str(round(db.execute('select sum(SUMA) from ECONOMIA where ACCION="INGRESO" and MES=? and DIA=?', (datetime.datetime.strptime(dd_mes.value,'%B').month, dd_dia.value)).fetchone()[0],2)), size=30)], alignment=MainAxisAlignment.CENTER)]
            c_ingresos.controls.append(Row([Text('DESCRIPCION', size=20, width=200), Text('SUMA', size=20, width=100)], alignment=MainAxisAlignment.CENTER))
            for ingreso in db.execute('select * from ECONOMIA where ACCION="INGRESO" and MES=? and DIA=?', (datetime.datetime.strptime(dd_mes.value,'%B').month, dd_dia.value)).fetchall():
                c_ingresos.controls.append(Container(content=Row([Text(ingreso[3], width=200), Text(ingreso[4], width=100)], alignment=MainAxisAlignment.CENTER), on_click=borra, bgcolor=colors.GREEN_50))
        else:c_ingresos.controls = [Row([Text(str(datetime.datetime(int(dd_año.value),datetime.datetime.strptime(dd_mes.value,'%B').month, int(dd_dia.value)).strftime('%A')) + ' ' + dd_dia.value + ' ' + dd_mes.value + ' ' + dd_año.value + ' TOT. €.0', size=30)], alignment=MainAxisAlignment.CENTER)]
        if db.execute('select sum(SUMA) from ECONOMIA where ACCION="GASTO" and MES=? and DIA=?', (datetime.datetime.strptime(dd_mes.value,'%B').month, dd_dia.value)).fetchone()[0] is not None:
            c_gastos.controls = [Row([Text(str(datetime.datetime(int(dd_año.value),datetime.datetime.strptime(dd_mes.value,'%B').month, int(dd_dia.value)).strftime('%A')) + ' ' + dd_dia.value + ' ' + dd_mes.value+ ' ' + dd_año.value + ' TOT. €.' + str(round(db.execute('select sum(SUMA) from ECONOMIA where ACCION="GASTO" and MES=? and DIA=?', (datetime.datetime.strptime(dd_mes.value,'%B').month, dd_dia.value)).fetchone()[0],2)), size=30)], alignment=MainAxisAlignment.CENTER)]
            c_gastos.controls.append(Row([Text('DESCRIPCION', size=20, width=200), Text('SUMA', size=20, width=100)], alignment=MainAxisAlignment.CENTER))
            for gasto in db.execute('select * from ECONOMIA where ACCION="GASTO" and MES=? and DIA=?', (datetime.datetime.strptime(dd_mes.value,'%B').month, dd_dia.value)).fetchall():
                c_gastos.controls.append(Container(content=Row([Text(gasto[3], width=200), Text(gasto[4], width=100)], alignment=MainAxisAlignment.CENTER), on_click=borra, bgcolor=colors.AMBER_50))
        else:c_gastos.controls = [Row([Text(str(datetime.datetime(int(dd_año.value),datetime.datetime.strptime(dd_mes.value,'%B').month, int(dd_dia.value)).strftime('%A')) + ' ' + dd_dia.value + ' ' + dd_mes.value + ' ' + dd_año.value + ' TOT. €.0', size=30)], alignment=MainAxisAlignment.CENTER)]
        db.close()
        page.update()
    def guarda(e):
        if dd_año.value!= '' and dd_mes.value!= '' and (dd_dia.value!= '') and (dd_accion.value!= '') and (t_descripcion.value!= '') and (t_suma.value!= ''):
            db = sqlite3.connect('ECONOMIA/' + dd_año.value + '.db')
            db.execute('insert into ECONOMIA values(?,?,?,?,?)', (dd_accion.value, datetime.datetime.strptime(dd_mes.value,'%B').month, dd_dia.value, t_descripcion.value.upper(), t_suma.value))
            db.commit()
            db.close()
            dd_accion.value, t_descripcion.value, t_suma.value = ('', '', 0.0)
            copia()
            muestra_dia('')
    def borra(e):
        values=[v.value for v in e.control.content.controls]
        db = sqlite3.connect('ECONOMIA/' + dd_año.value + '.db')
        if len(values) == 5:
            values[2] = datetime.datetime.strptime(values[2], '%B').month
            db.execute('delete from ECONOMIA where DIA=? and MES=? and DESCRIPCION=? and SUMA=?', values[1:])
            db.commit()
            db.close()
            copia()
            muestra_año('')
        elif len(values) == 4:
            values[0]=datetime.datetime.strptime(dd_mes.value,'%B').month
            db.execute('delete from ECONOMIA where MES=? and DIA=? and DESCRIPCION=? and SUMA=?',values)
            db.commit()
            db.close()
            copia()
            muestra_mes('')
        elif len(values) == 2:
            db.execute('delete from ECONOMIA where MES=? and DIA=? and DESCRIPCION=? and SUMA=?', (datetime.datetime.strptime(dd_mes.value,'%B').month,dd_dia.value,values[0],values[1],))
            db.commit()
            db.close()
            copia()
            muestra_dia('')
    def copia():
        if os.path.exists('/Users/tommylatorre/Desktop/ARCHIVO/ECONOMIA'):shutil.rmtree('/Users/tommylatorre/Desktop/ARCHIVO/ECONOMIA')
        shutil.copytree('ECONOMIA', '/Users/tommylatorre/Desktop/ARCHIVO/ECONOMIA')
    page.window.full_screen = True
    page.theme_mode = ThemeMode.LIGHT
    dd_año = Dropdown(label='AÑO', options=[dropdown.Option(a[:(-3)]) for a in os.listdir('ECONOMIA')], on_change=muestra_año)
    dd_mes = Dropdown(label='MES', options=[dropdown.Option((datetime.datetime(2024,m,1).strftime('%B')).upper()) for m in meses], on_change=muestra_mes, disabled=True)
    dd_dia = Dropdown(label='DIA', on_change=muestra_dia, disabled=True)
    c_ingresos = Column(width=600, height=450, scroll=ScrollMode.ALWAYS)
    c_gastos = Column(width=600, height=450, scroll=ScrollMode.ALWAYS)
    dd_accion = Dropdown(label='ACCION', options=[dropdown.Option('INGRESO'), dropdown.Option('GASTO')], on_change=lambda _: guarda)
    t_descripcion = TextField(label='DESCRIPCION')
    t_suma = TextField(label='SUMA', value=0.0)
    page.add(Row([IconButton(icon=icons.EXIT_TO_APP, icon_color='red', icon_size=50, on_click=lambda _: page.window.destroy())], alignment=MainAxisAlignment.END),
             Row([dd_año, dd_mes, dd_dia], alignment=MainAxisAlignment.CENTER),
             Row([Row([Text('INGRESOS', size=40)], alignment=MainAxisAlignment.CENTER, width=600),Row([Text('GASTOS', size=40)], alignment=MainAxisAlignment.CENTER, width=600)]),
             Row([c_ingresos, VerticalDivider(), c_gastos], height=450), Divider(),
             Row([dd_accion, t_descripcion, t_suma, ElevatedButton('GUARDA', on_click=guarda)], alignment=MainAxisAlignment.CENTER))
    page.update()
app(target=main)