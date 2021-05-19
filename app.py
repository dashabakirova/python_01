from math import log10, pi
from tkinter import *
from tkinter import messagebox
from tkFastCoding import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from functools import partial
import json


class MyWindow:
    objects = []
    # В параметре 'parametrs' объекта индекс 0 - значение v, индекс 1 - q, индекс 2 - k, индекс 3 - prop (доля)
    browsed_object = ()

    def __init__(self, win):
        # переменная для хранения объектов
        self.win = win

        # переменные окна ввода параметров НПС
        self.lb_v, self.inp_v, self.lb_prop, self.lb_q, self.inp_q = [], [], [], [], []
        self.btn_del, self.lb_source_q, self.jj = [], [], []
        self.lb_a, self.lb_b, self.lb_n, self.lb_z = [], [], [], []
        self.inp_a, self.inp_b, self.inp_n, self.inp_z = [], [], [], []
        self.outputs = []
        self.lb_available, self.lb_sum_prop, self.lb_remain = None, None, None

        # переменные окна вязкости
        self.viscosity_win = None
        self.lb_v_vs, self.inp_k = [], []

        # параметры холста
        self.canvas = packObject(Canvas, win, 0, 0, {"bg": "white", "bd": 2, "width": 900, "height": 598})
        self.canvas.create_rectangle(0, 0, 1000, 698, fill="white")

        # Лейблы
        self.lb_object = packObject(Label, win, 920, 30, {"text": "Объект"})
        self.lb_event = packObject(Label, win, 920, 100, {"text": "Действие"})
        self.lb_obj_param = packObject(Label, win, 920, 170, {"text": "Параметры объекта"})
        self.lb_tp_length = packObject(Label, win, 940, 260, {"text": "Длина L, км:"})
        self.lb_NPC1 = packObject(Label, win, 940, 195, {"text": "НПС 1:"})
        self.lb_NPC2 = packObject(Label, win, 940, 225, {"text": "НПС 2:"})
        self.lb_diameter = packObject(Label, win, 940, 290, {"text": 'Диаметр, мм:'})
        self.lb_G = packObject(Label, win, 940, 320, {"text": 'G, млн.т:'})
        self.lb_id = packObject(Label, win, 940, 195, {"text": "id:"})
        self.lb_name = packObject(Label, win, 940, 225, {"text": 'Название:'})
        # self.lb_len_point = packObject(Label, win, 940, 255, {"text": 'Высота отметки, z:'})
        self.lb_inputs = packObject(Label, win, 940, 285, {"text": 'Вход:'})
        self.lb_outputs = packObject(Label, win, 940, 315, {"text": 'Выход:'})
        # self.lb_param_a = packObject(Label, win, 940, 345, {"text": 'Параметр a:'})
        # self.lb_param_b = packObject(Label, win, 940, 375, {"text": 'Параметр b:'})
        # self.lb_param_n = packObject(Label, win, 940, 405, {"text": 'Параметр n:'})
        # self.lb_param_t = packObject(Label, win, 940, 435, {"text": 'Параметр t:'})
        self.lb_param_t = packObject(Label, win, 940, 345, {"text": 'Параметр t:'})

        self.lb_Q = packObject(Label, win, 1040, 470, {"text": "Q = "})
        self.lb_V = packObject(Label, win, 1040, 440, {"text": "V = "})

        # Определение типов данных формы
        self.inp_id = StringVar(win)
        self.inp_name = StringVar(win)
        self.inp_tp_lenth = StringVar(win)
        # self.inp_param_a = StringVar(win)
        # self.inp_param_b = StringVar(win)
        # self.inp_param_n = StringVar(win)
        self.inp_param_t = StringVar(win)
        self.inp_tp_first = StringVar(win)
        self.inp_tp_second = StringVar(win)
        # self.inp_lenghPoint = StringVar(win)
        self.edit_vert5 = StringVar(win)
        self.inp_tp_diameter = StringVar(win)
        self.inp_tp_G = StringVar(win)
        self.radio1, self.radio2 = IntVar(), IntVar()

        # Поля ввода данных формы
        self.id = packObject(Entry, win, 1070, 195, {"width": "10", "textvariable": self.inp_id})
        self.name = packObject(Entry, win, 1070, 225, {"width": "10", "textvariable": self.inp_name})
        # self.npc_lenthPoint = packObject(Entry, win, 1070, 255, {"width": "10", "textvariable": self.inp_lenghPoint})
        # self.param_a = packObject(Entry, win, 1070, 345, {"width": "10", "textvariable": self.inp_param_a})
        # self.param_b = packObject(Entry, win, 1070, 375, {"width": "10", "textvariable": self.inp_param_b})
        # self.param_n = packObject(Entry, win, 1070, 405, {"width": "10", "textvariable": self.inp_param_n})
        # self.param_t = packObject(Entry, win, 1070, 435, {"width": "10", "textvariable": self.inp_param_t})
        self.param_t = packObject(Entry, win, 1070, 345, {"width": "10", "textvariable": self.inp_param_t})

        self.tp_first = packObject(Entry, win, 1070, 195, {"width": "10", "textvariable": self.inp_tp_first})
        self.tp_second = packObject(Entry, win, 1070, 225, {"width": "10", "textvariable": self.inp_tp_second})
        self.tp_diameter = packObject(Entry, win, 1070, 290, {"width": "10", "textvariable": self.inp_tp_diameter})
        self.tp_G = packObject(Entry, win, 1070, 320, {"width": "10", "textvariable": self.inp_tp_G})
        self.tp_lenth = packObject(Entry, win, 1070, 260, {"width": "10", "textvariable": self.inp_tp_lenth})

        # Радиометки
        # self.r1 = packObject(Radiobutton, win, 940, 30, {"variable": self.radio1, "text": "НПС", "value": 0,
        #                                                  "command": self.updateParametrs})
        self.r5 = packObject(Radiobutton, win, 940, 50, {"variable": self.radio1, "text": "НПС c резервуарным парком",
                                                         "value": 1, "command": self.updateParametrs})
        self.r2 = packObject(Radiobutton, win, 940, 70, {"variable": self.radio1, "text": "Трубопровод", "value": 2,
                                                         "command": self.updateParametrs})
        self.r3 = packObject(Radiobutton, win, 940, 120, {"variable": self.radio2, "text": "Добавление", "value": 0,
                                                          "command": self.updateParametrs})
        self.r4 = packObject(Radiobutton, win, 940, 140, {"variable": self.radio2, "text": "Изменить", "value": 1,
                                                          "command": self.updateParametrs})

        # Кнопки
        self.btn_add_object = packObject(Button, win, 940, 380, {
            "width": "12", "height": "1", "text": "Добавить", "command": self.add_object
        })
        self.btn_calc_V = packObject(Button, win, 940, 440, {
            "width": "12", "height": "1", "text": "Рассчитать V", "command": self.calc_v
        })
        self.btn_add_param = packObject(Button, win, 940, 470, {
            "width": "12", "height": "1", "text": "Добавить q, v", "command": self.param_npc
        })
        self.btn_calc_Q = packObject(Button, win, 940, 470, {
            "width": "12", "height": "1", "text": "Рассчитать Q", "command": self.calc_q
        })
        self.btn_update_object = packObject(Button, win, 940, 500, {
            "width": "12", "height": "1", "text": "Обновить", "command": self.editobject
        })
        self.btn_remove_object = packObject(Button, win, 1040, 500, {
            "width": "12", "height": "1", "text": "Удалить", "command": self.removeobject
        })
        self.btn_clear = packObject(Button, win, 940, 530, {
            "width": "12", "height": "1", "text": "Очистить", "command": self.clear
        })
        self.btn_viscosity = packObject(Button, win, 1040, 530, {
            "width": "12", "height": "1", "text": "Вязкость", "command": self.viscosity
        })
        self.btn_conf_import = packObject(Button, win, 1040, 560, {
            "width": "12", "height": "1", "text": "Открыть", "command": self.import_conf
        })
        self.btn_conf_export = packObject(Button, win, 940, 560, {
            "width": "12", "height": "1", "text": "Сохранить", "command": self.export_conf
        })
        self.btn_calculate = packObject(Button, win, 940, 590, {
            "width": "26", "height": "1", "text": "Выполнить расчёт", "command": self.calculate
        })

        # События
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.rclick)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<B1-Motion>", self.drop)
        self.canvas.bind("<Delete>", self.removeobject)
        self.updateParametrs()

        # Значения данных формы
        # self.inp_tp_second.set(0)
        self.inp_tp_first.set(0)
        self.inp_tp_second.set(0)
        # self.inp_lenghPoint.set(0)
        self.inp_id.set(0)
        self.inp_tp_lenth.set(0)
        self.inp_tp_diameter.set(0)
        self.inp_tp_G.set(0)
        self.radio1.set(0)
        self.radio2.set(0)

        # Переменная для хранения параметра "c"
        self.c = -4.5

    def calculate(self):
        # Расчёт долей и t
        curr_obj = self.browsed_object
        npc_list = [obj for obj in self.objects if obj['type'] == 'NPC_RP']
        for npc in npc_list:
            self.browsed_object = npc
            self.calc_prop(self.browsed_object, 0, save_flag=True)
        self.browsed_object = curr_obj

        tp_list = [obj for obj in self.objects if obj['type'] == 'tp']

        # Расчёт V
        for tp in tp_list:
            self.calc_v(source_id=tp['npc1'], target_id=tp['npc2'])

        # Расчёт Q
        for tp in tp_list:
            self.calc_q(source_id=tp['npc1'], target_id=tp['npc2'])

        # Сообщение о завершении выполнения расчёта
        messagebox.showinfo('Расчёт завершён', 'Процедура расчёта завершена!')

    def calc_v(self, source_id=None, target_id=None):
        self.lb_V['text'] = 'Рассчитываю...'
        v = 0
        if source_id is None and target_id is None:
            source_id = self.inp_tp_first.get()
            target_id = self.inp_tp_second.get()
        tp = self.getTP(source_id, target_id)
        if tp:
            target = self.getObj(target_id)
            try:
                t = float(self.objects[int(source_id) - 1]['param_t'])
            except:
                t = 0
            c = float(self.c)
            v_min, v_max = self.min_max_v()
            try:
                v = pow(10, log10(v_min + c) * (1 - t) + log10(v_max + c) * t) - c
            except:
                pass
            if 'input_qv' not in target:
                target['input_qv'] = {}
            target['input_qv']['v'] = v
            self.canvas_update()
        self.lb_V['text'] = 'Рассчитано'

    # функция расчета напора
    def calc_q(self, source_id=None, target_id=None):
        self.lb_Q['text'] = 'Рассчитываю...'
        # q = 0
        if source_id is None and target_id is None:
            source_id = self.inp_tp_first.get()
            target_id = self.inp_tp_second.get()
        tp = self.getTP(source_id, target_id)
        if tp:
            source = self.getObj(source_id)
            target = self.getObj(target_id)
            if source:
                a = float(source['abnz'][target_id]['a'])
                b = float(source['abnz'][target_id]['b'])
                n = float(source['abnz'][target_id]['n'])
                z = float(source['abnz'][target_id]['z'])
                # a = float(source['param_a'])
                # b = float(source['param_b'])
                # n = float(source['param_n'])
                # z = float(source['lenghPoint'])
                m1 = 0.25
                b1 = 0.0246
                L = float(tp['tp_lenth']) * 1000
                D = float(tp['diameter']) / 1000
                v = 0

                source_outputs = self.getObjOutputByTPs(source_id)
                for sourceOutput in source_outputs:
                    if sourceOutput['to'] == target_id:
                        v = int(float(sourceOutput['v'])) * 0.000001
                q = pow(((n * a - z) / (-b * n + 1.02 * b1 * (v ** m1) * L / (D ** (5 - m1)))), 1 / (2 - m1))
                # Q = -((- b - B1 * L * (D ** (m1-5)) * (v ** m1))/(a)) ** (m1-2)
                re = (4 * q) / (pi * D * v)
                if re >= (17.5 * D / 0.0002):
                    m1 = 0.1
                    b1 = 0.0166 / pow((0.0002 / D), 0.15)
                    q = pow(((n * a - z) / (-b * n + 1.02 * b1 * (v ** m1) * L / (D ** (5 - m1)))), 1 / (2 - m1))
                # if len(target['parametrs']) == 0:
                #     target['parametrs'].append(['0', '0', '0', '0'])
                if 'input_qv' not in target:
                    target['input_qv'] = {}
                target['input_qv']['q'] = q
                self.canvas_update()
        self.lb_Q['text'] = 'Рассчитано'
        # return 0

    def viscosity(self):
        self.viscosity_win = Toplevel()
        self.viscosity_win.title('Вязкость')
        self.viscosity_win.resizable(width=False, height=True)
        self.lb_v_vs = []
        self.inp_k = []
        packObject(Label, self.viscosity_win, 20, 10, {"text": 'Свойства:'})

        start_y = 40
        counter = 0
        # v_set = set()
        for obj in self.objects:
            if obj['type'] == 'NPC_RP':
                for param in obj['parametrs']:
                    self.input_k = StringVar(self.viscosity_win)
                    # v_set.add(int(param[0]))
                    packObject(Label, self.viscosity_win, 20, start_y + counter * 25, {"text": f'v{counter + 1}='})
                    v = packObject(Label, self.viscosity_win, 60, start_y + counter * 25, {"text": param[0]})
                    packObject(Label, self.viscosity_win, 120, start_y + counter * 25, {"text": f'k{counter + 1}='})
                    entry = packObject(Entry, self.viscosity_win, 160, start_y + counter * 25,
                                       {"width": "10", "textvariable": self.input_k})
                    self.lb_v_vs.append(v)
                    self.inp_k.append(entry)
                    self.input_k.set(param[2])
                    counter += 1

        v_min, v_max = self.min_max_v()
        packObject(Label, self.viscosity_win, 20, start_y + counter * 25, {"text": f'v min = {v_min}'})
        packObject(Label, self.viscosity_win, 20, start_y + (counter + 1) * 25, {"text": f'v max = {v_max}'})

        for index in range(len(self.inp_k)):
            if float(self.lb_v_vs[index].cget('text')) == v_min:
                self.inp_k[index].delete(0, END)
                self.inp_k[index].insert(0, 0)
                self.inp_k[index].configure(state='disabled')
            elif float(self.lb_v_vs[index].cget('text')) == v_max:
                self.inp_k[index].delete(0, END)
                self.inp_k[index].insert(0, 1)
                self.inp_k[index].configure(state='disabled')

        self.input_c = StringVar(self.viscosity_win)
        packObject(Label, self.viscosity_win, 120, start_y + (counter + 2) * 25, {"text": 'c ='})
        self.inp_c = packObject(Entry, self.viscosity_win, 160, start_y + (counter + 2) * 25,
                                {"width": "10", "textvariable": self.input_c})
        self.input_c.set(self.c)

        self.btn_ok = packObject(Button, self.viscosity_win, 20, start_y + (counter + 3) * 25, {
            "width": "12", "height": "1", "text": "Ок", "command": self.save_k
        })
        self.viscosity_win.geometry(f"250x{start_y + (counter + 3) * 25 + 40}")

    def min_max_v(self):
        v_set = set()
        for obj in self.objects:
            if obj['type'] == 'NPC_RP':
                for param in obj['parametrs']:
                    v_set.add(float(param[0]))
        return min(v_set), max(v_set)

    def save_k(self):
        self.c = self.input_c.get()
        counter = 0
        for obj in self.objects:
            if obj['type'] == 'NPC_RP':
                for param in obj['parametrs']:
                    if len(param) == 2:
                        param.append(self.inp_k[counter].get())
                    else:
                        param[2] = self.inp_k[counter].get()
                    counter += 1
        self.viscosity_win.destroy()

    def param_npc(self):
        if self.browsed_object != () and self.browsed_object['type'] == 'NPC_RP':
            self.param_win = Toplevel()
            self.param_win.title('Параметры')
            self.param_win.resizable(width=False, height=True)
            self.update_win_param()

            if self.browsed_object != ():
                packObject(Label, self.param_win, 40, 10, {"text": f'Параметры объекта {self.browsed_object["id"]}'})

                self.btn_add_parametrs = packObject(Button, self.param_win, 20, 40, {
                    "width": "12", "height": "1", "text": "Добавить", "command": self.add_param
                })
                self.btn_update_parametrs = packObject(Button, self.param_win, 120, 40, {
                    "width": "12", "height": "1", "text": "Обновить", "command": self.upd_param
                })
                calc_prop = partial(self.calc_prop, self.browsed_object, 0)
                self.btn_calc_prop = packObject(Button, self.param_win, 240, 40, {
                    "width": "12", "height": "1", "text": "Доли", "command": calc_prop
                })

    def add_param(self):
        for n, i in enumerate(self.objects):
            if i['type'] == 'NPC_RP' and i['id'] == self.browsed_object['id']:
                self.objects[n]['parametrs'].append(['0', '0', '0', '0'])

        self.update_win_param()
        self.canvas_update()

        self.param_win.destroy()
        self.param_npc()

    def upd_param(self):
        k = [params[2] for params in self.browsed_object['parametrs']]
        for n, i in enumerate(self.objects):
            if i['type'] == 'NPC_RP' and i['id'] == self.browsed_object['id']:
                for v, q in zip(self.inp_v, self.inp_q):
                    self.objects[n]['parametrs'].clear()
                self.objects[n]['abnz'] = {}

        if len(self.inp_v) < len(k):
            k = k[0:len(self.inp_v)]
        elif len(self.inp_v) > len(k):
            k.extend(['0' for i in range(len(self.inp_v) - len(k))])

        for n, i in enumerate(self.objects):
            if i['type'] == 'NPC_RP' and i['id'] == self.browsed_object['id']:
                index = 0
                for v, q, prop in zip(self.inp_v, self.inp_q, self.lb_prop):
                    self.objects[n]['parametrs'].append([v.get(), q.get(), k[index], prop.cget('text')])
                    index += 1
                for out, a, b, inp_n, z in zip(self.outputs, self.inp_a, self.inp_b, self.inp_n, self.inp_z):
                    self.objects[n]['abnz'][out] = {'a': a.get(), 'b': b.get(), 'n': inp_n.get(), 'z': z.get()}

        self.update_win_param()
        self.canvas_update()

        self.param_win.destroy()
        self.param_npc()

    # функция расчёта долей (рекурсивная)
    def calc_prop(self, current_object, counter, save_flag=False):
        # save_flag - если True, значит работаем по кнопке "Выполнить расчёт". В этом случае у стартовой НПС доли не
        # выводятся на форму, а записываются в объект
        source = self.getObjInputByTPs(current_object['id'])
        t = 0
        sum_prop = 0
        if len(source) > 0:
            # Было
            # source_q = float(source[0]['q'])
            # Стало
            obj_ = None
            for obj in self.objects:
                if obj['id'] == source[0]['from']:
                    obj_ = obj
                    t_, counter, sum_prop_ = self.calc_prop(obj_, counter, save_flag)
                    t += t_
                    sum_prop += sum_prop_
                    break
            in_G, sum_G = self.in_out_g(current_object)
            source_q = 0
            # index = 0
            if sum_G > 0:
                for params in obj_['parametrs']:
                    new_prop = float(params[3]) * in_G / sum_G
                    sum_prop += new_prop
                    # new_prop = float(param[1]) * float(param[3]) / sum_G
                    # if current_object['id'] == self.browsed_object['id']:
                    #     self.lb_source_q[index].config(text=f'q{index + 1} = ' + params[1] + f' ({new_prop})')
                    # else:
                    #     params[3] = new_prop
                    if not save_flag:
                        current_text = self.lb_source_q[counter].cget('text').split(' = ')
                        self.lb_source_q[counter].config(text=current_text[0] + ' = ' + params[1] + f' ({new_prop})')
                    # params[3] = new_prop
                    source_q += new_prop
                    counter += 1
                    # index += 1
            # if current_object['id'] == self.browsed_object['id']:
                # self.lb_sum_prop.config(text=f'Сумма долей = ({sum_prop})')
                # self.lb_remain.config(text=f'Осталось = ({1 - sum_prop})')
                # self.lb_sum_prop.config(text=f'Сумма долей = ({source_q})')
                # self.lb_remain.config(text=f'Осталось = ({1 - source_q})')
        else:
            source_q = 0

        sum_q = 0
        # Если работаем с текущим НПС, то значения берём из полей ввода, иначе - из списка параметров
        if current_object['id'] == self.browsed_object['id'] and not save_flag:
            for index in range(len(self.inp_q)):
                sum_q += float(self.inp_q[index].get())
            index = 0
            for lb_prop in self.lb_prop:
                curr_q = float(self.inp_q[index].get())
                sum_prop += curr_q / (source_q + sum_q)
                lb_prop.config(text=str(round(curr_q / (source_q + sum_q), 3)))
                index += 1
            for index in range(len(self.lb_prop)):
                t += float(self.lb_prop[index].cget('text')) * float(current_object['parametrs'][index][2])
            # self.lb_sum_prop.config(text=f'Сумма долей = ({source_q + sum_q})')
            # self.lb_remain.config(text=f'Осталось = ({1 - source_q - sum_q})')
            self.lb_sum_prop.config(text=f'Сумма долей = ({sum_prop})')
            self.lb_remain.config(text=f'Осталось = ({1 - sum_prop})')
            self.inp_param_t.set(t)
        else:
            for params in current_object['parametrs']:
                sum_q += float(params[1])
            for params in current_object['parametrs']:
                if save_flag:
                    params[3] = str(float(params[1]) / (source_q + sum_q))
                t += float(params[1]) / (source_q + sum_q) * float(params[2])

        current_object['param_t'] = t
        return t, counter, sum_prop

    def in_out_g(self, current_object):
        source = self.getObjInputByTPs(current_object['id'])
        if len(source) > 0:
            tp = self.getTP(source[0]['from'], source[0]['to'])
            in_G = float(tp['tp_G']) * 1000000000 / (24 * 350 * 800)
        else:
            in_G = 0
        links_out = self.getObjLinksByTP(current_object['id'], 'output')
        sum_G = 0
        for link in links_out:
            tp = self.getTP(current_object['id'], link['obj']['id'])
            sum_G += float(tp['tp_G']) * 1000000000 / (24 * 350 * 800)
        return in_G, sum_G

    def remove_param(self, n):
        for j, i in enumerate(self.objects):
            if i['type'] == 'NPC_RP' and i['id'] == self.browsed_object['id']:
                self.objects[j]['parametrs'].pop(n)

        self.update_win_param()
        self.canvas_update()

        self.param_win.destroy()
        self.param_npc()

    def update_win_param(self):
        s = 0
        self.heith = 120
        self.noheith = 200
        j = 40

        self.lb_v, self.inp_v, self.lb_prop, self.lb_q, self.inp_q = [], [], [], [], []
        self.btn_del, self.lb_source_q, self.jj = [], [], []
        self.lb_a, self.lb_b, self.lb_n, self.lb_z = [], [], [], []
        self.inp_a, self.inp_b, self.inp_n, self.inp_z = [], [], [], []
        self.outputs = []

        self.lb_v.append(packObject(Label, self.param_win, 10, 80 + s, {"text": f'Входы:'}))
        s += 40
        self.heith += 40

        # Подсчитываем, какими по порядку будут q, v для выбранного объекта
        counter = 0
        for obj in self.objects:
            if obj['type'] == 'NPC_RP' and int(obj['id']) < int(self.browsed_object['id']):
                counter += len(obj['parametrs'])

        for i, obj in enumerate(self.browsed_object['parametrs']):
            self.jj.append(i)
            self.input_v = StringVar(self.param_win)
            self.input_q = StringVar(self.param_win)

            self.lb_v.append(packObject(Label, self.param_win, 10, 80 + s, {"text": f'v{counter + 1}:'}))
            self.inp_v.append(
                packObject(Entry, self.param_win, 40, 80 + s, {"width": "10", "textvariable": self.input_v}))
            self.lb_q.append(packObject(Label, self.param_win, 110, 80 + s, {"text": f'q{counter + 1}:'}))
            self.inp_q.append(
                packObject(Entry, self.param_win, 140, 80 + s, {"width": "10", "textvariable": self.input_q}))
            action_with_arg = partial(self.remove_param, i)
            self.btn_del.append(packObject(Button, self.param_win, 210, 75 + s, {"width": "2", "height": "1",
                                                                                 "text": "del",
                                                                                 "command": action_with_arg}))
            self.lb_prop.append(packObject(Label, self.param_win, 250, 80 + s, {"text": '0'}))
            counter += 1
            self.input_v.set(obj[0])
            self.input_q.set(obj[1])

            self.lb_prop[-1].config(text=obj[3])
            j += 40
            s += 40
            self.heith += 40
            self.noheith -= 0

        # возможно добавить
        in_g, sum_g = self.in_out_g(self.browsed_object)
        available = int(sum_g - in_g)
        self.lb_available = packObject(Label, self.param_win, 110, 80 + s, {"text": f'Возможно добавить: {available}'})
        s += 20

        # доли предыдущих НПС
        sources = self.get_sources_chain(self.browsed_object, [])
        counter = 0
        sum = 0
        for obj in self.objects:
            if obj['type'] == 'NPC_RP' and int(obj['id']) < int(self.browsed_object['id']):
                if obj in sources:
                    for params in obj['parametrs']:
                        sum += float(params[3])
                        counter += 1
                        self.lb_source_q.append(packObject(Label, self.param_win, 110, 80 + s,
                                                           {"text": f'q{counter} = ' + params[1] + f' ({params[3]})'}))
                        s += 20
                        self.heith += 20
                else:
                    counter += len(obj['parametrs'])
        for params in self.browsed_object['parametrs']:
            sum += float(params[3])
        self.lb_sum_prop = packObject(Label, self.param_win, 110, 80 + s, {"text": f'Сумма долей = ({sum})'})
        s += 20
        self.heith += 20
        self.lb_remain = packObject(Label, self.param_win, 110, 80 + s, {"text": f'Осталось = ({1 - sum})'})
        s += 20
        self.heith += 20

        # Входы q,v
        tp_inputs = self.getObjInputByTPs(self.browsed_object['id'])
        # self.lb_v.append(packObject(Label, self.param_win, 10, 80 + s, {"text": f'Входы:'}))
        s += 30
        self.heith += 30
        for tpInput in tp_inputs:
            input_text = 'v' + str(tpInput['from']) + '-' + str(tpInput['to']) + ': ' + str(tpInput['v'])
            self.lb_v.append(packObject(Label, self.param_win, 10, 80 + s, {"text": input_text}))
            input_text = 'q' + str(tpInput['from']) + '-' + str(tpInput['to']) + ': ' + str(tpInput['q'])
            self.lb_q.append(packObject(Label, self.param_win, 110, 80 + s, {"text": input_text}))
            s += 30
            self.heith += 30

        # Выходы q,v
        tp_outputs = self.getObjOutputByTPs(self.browsed_object['id'])
        self.lb_v.append(packObject(Label, self.param_win, 10, 80 + s, {"text": f'Выходы:'}))
        s += 30
        self.heith += 30
        for tpOutput in tp_outputs:
            self.input_a = StringVar(self.param_win)
            self.input_b = StringVar(self.param_win)
            self.input_n = StringVar(self.param_win)
            self.input_z = StringVar(self.param_win)
            self.outputs.append(tpOutput['to'])
            output_text = 'v' + str(tpOutput['from']) + '-' + str(tpOutput['to']) + ': ' + str(tpOutput['v'])
            self.lb_v.append(packObject(Label, self.param_win, 10, 80 + s, {"text": output_text}))
            output_text = 'q' + str(tpOutput['from']) + '-' + str(tpOutput['to']) + ': ' + str(tpOutput['q'])
            self.lb_q.append(packObject(Label, self.param_win, 110, 80 + s, {"text": output_text}))

            self.lb_a.append(packObject(Label, self.param_win, 210, 80 + s, {"text": 'a: '}))
            self.inp_a.append(
                packObject(Entry, self.param_win, 230, 80 + s, {"width": "10", "textvariable": self.input_a}))
            self.lb_b.append(packObject(Label, self.param_win, 310, 80 + s, {"text": 'b: '}))
            self.inp_b.append(
                packObject(Entry, self.param_win, 330, 80 + s, {"width": "10", "textvariable": self.input_b}))
            self.lb_n.append(packObject(Label, self.param_win, 410, 80 + s, {"text": 'n: '}))
            self.inp_n.append(
                packObject(Entry, self.param_win, 430, 80 + s, {"width": "10", "textvariable": self.input_n}))
            self.lb_z.append(packObject(Label, self.param_win, 510, 80 + s, {"text": 'z: '}))
            self.inp_z.append(
                packObject(Entry, self.param_win, 530, 80 + s, {"width": "10", "textvariable": self.input_z}))
            a, b, n, z = 0, 0, 0, 0

            if 'abnz' in self.browsed_object:
                if tpOutput['to'] in self.browsed_object['abnz']:
                    a = self.browsed_object['abnz'][tpOutput['to']]['a']
                    b = self.browsed_object['abnz'][tpOutput['to']]['b']
                    n = self.browsed_object['abnz'][tpOutput['to']]['n']
                    z = self.browsed_object['abnz'][tpOutput['to']]['z']
            self.input_a.set(a)
            self.input_b.set(b)
            self.input_n.set(n)
            self.input_z.set(z)

            s += 30
            self.heith += 30

        self.param_win.geometry(f"600x{self.heith}+500+{self.noheith}")

    def get_sources_chain(self, current_object, sources):
        source = self.getObjLinksByTP(current_object['id'], 'input')
        if len(source) > 0:
            obj_ = source[0]['obj']
            self.get_sources_chain(obj_, sources)
            sources.append(obj_)
            return sources

    def rclick(self, e):
        d = 1000000
        for i in self.objects:
            if i['type'] == 'NPC' and self.radio2.get() == 0 and self.radio1.get() == 2:
                if sqr(self.X - i["x"]) + sqr(self.Y - i["y"]) < d:
                    d = sqr(self.X - i["x"]) + sqr(self.Y - i["y"])
                    self.browsed_object = i
                    self.updateParametrs()
                    self.inp_tp_second.set(self.browsed_object['id'])

            elif i['type'] == 'NPC_RP' and self.radio2.get() == 0 and self.radio1.get() == 2:
                if sqr(self.X - i["x"]) + sqr(self.Y - i["y"]) < d:
                    d = sqr(self.X - i["x"]) + sqr(self.Y - i["y"])
                    self.browsed_object = i
                    self.updateParametrs()
                    self.inp_tp_second.set(self.browsed_object['id'])

        if self.inp_tp_first.get() != self.inp_tp_second.get():
            self.add_object()

        self.canvas_update()

    def canvas_update(self):
        self.canvas.create_rectangle(0, 0, 1000, 668, fill="white")
        v1 = self.tp_first.get()
        v2 = self.tp_second.get()
        list_npc = [i['id'] for i in self.objects if i['type'] == 'NPC' or i['type'] == 'NPC_RP']
        filling = "black"

        counter = 0
        for obj in self.objects:

            # меняет цвет выбранного объекта
            filling = "black"
            if self.radio1.get() <= 1 and self.radio2.get() == 1:
                if 'id' in obj and obj['id'] == self.inp_id.get():
                    filling = "#AAAAAA"
            if self.radio1.get() == 2:
                if 'npc1' in obj:
                    if obj['npc1'] == self.inp_tp_first.get() and obj['npc2'] == self.inp_tp_second.get():
                        filling = "#AAAAAA"
                else:
                    if obj['id'] == self.inp_tp_first.get() or obj['id'] == self.inp_tp_second.get():
                        filling = "#AAAAAA"

            if obj['type'] == 'NPC':
                self.canvas.create_oval(
                    obj["x"] - 15, obj["y"] - 15, obj["x"] + 15, obj["y"] + 15, fill=filling, tag=obj['id'])
                self.canvas.create_arc(
                    obj["x"] - 15, obj["y"] - 15, obj["x"] + 15, obj["y"] + 15, start=45, extent=90,
                    fill="white", tag=obj['id'])
                self.canvas.create_arc(
                    obj["x"] - 15, obj["y"] - 15, obj["x"] + 15, obj["y"] + 15, start=225, extent=90,
                    fill="white", tag=obj['id'])
                self.canvas.create_text(obj["x"] + 35, obj["y"] - 20,
                                        text=obj["name"] + " (" + obj["id"] + ")" + "\n" + "Z: "
                                             + obj["lenghPoint"] + "\n" + "a: " + obj["param_a"] + "\n" + "b: "
                                             + obj["param_b"] + "\n" + "n: " + obj["param_n"], fill="red")

            elif obj['type'] == 'NPC_RP':
                qv = ''
                qv_ots = 40

                for n, i in enumerate(obj['parametrs']):
                    qv += f"v{counter + 1}:" + str(i[0])
                    qv += f" q{counter + 1}:" + str(i[1]) + "\n"
                    qv_ots += 10
                    counter += 1

                self.canvas.create_oval(
                    obj["x"] - 15, obj["y"] - 15, obj["x"] + 15, obj["y"] + 15, fill=filling, tag=obj['id'])
                self.canvas.create_arc(
                    obj["x"] - 15, obj["y"] - 15, obj["x"] + 15, obj["y"] + 15, start=45, extent=90,
                    fill="white", tag=obj['id'])
                self.canvas.create_arc(
                    obj["x"] - 15, obj["y"] - 15, obj["x"] + 15, obj["y"] + 15, start=225, extent=90,
                    fill="white", tag=obj['id'])
                # стрелка
                self.canvas.create_line(
                    obj["x"], obj["y"] - 20, obj["x"], obj["y"] - 50,
                    obj["x"], obj["y"] - 20, obj["x"] + 4, obj["y"] - 28,
                    obj["x"], obj["y"] - 20, obj["x"] - 4, obj["y"] - 28)
                self.canvas.create_line(
                    obj["x"] + 15, obj["y"] + 16, obj["x"] + 30, obj["y"] + 16,
                    obj["x"] + 30, obj["y"] + 25, obj["x"] + 15, obj["y"] + 25,
                    obj["x"] + 15, obj["y"] + 16, obj["x"] + 23, obj["y"] + 10,
                    obj["x"] + 30, obj["y"] + 16, fill="black")
                # self.canvas.create_text(obj["x"] + 40, obj["y"] - qv_ots, text=obj["name"] + " (" + obj["id"] + ")" + "\n"
                # + "Z: " + obj["lenghPoint"] + "\n" + "a: " + obj["param_a"] + "\n" + "b: "
                # + obj["param_b"] + "\n" + "n: " + obj["param_n"] + "\n"  + qv, fill="red")
                self.canvas.create_text(obj["x"] + 40, obj["y"] - qv_ots, text=obj["name"] + " (" + obj["id"] + ")"
                                                                               + "\n" + qv, fill="red")

            elif obj['type'] == 'tp':
                # проверяем присутствуют ли npc1 и npc2 в списке объектов
                if obj['npc1'] in list_npc and obj['npc1'] in list_npc:
                    for el in self.objects:
                        if el['type'] == 'NPC' or el['type'] == 'NPC_RP':
                            if el['id'] == obj['npc1']:
                                v1 = el

                        if el['type'] == 'NPC' or el['type'] == 'NPC_RP':
                            if el['id'] == obj['npc2']:
                                v2 = el

                    cse = CSE(15, v1["x"], v1["y"], v2["x"], v2["y"])

                    self.canvas.create_line(cse[0], cse[1], cse[2], cse[3], fill=filling, width=3, arrow=LAST,
                                            arrowshape="5 10 5")

                    x_p, y_p = 0, 0

                    if abs(v1['x'] - v2['x']) < 60:
                        x_p = 20
                    else:
                        y_p = 40

                    display_G = int(float(obj['tp_G']) * 1000000000 / (24 * 350 * 800))
                    self.canvas.create_text((v1["x"] + v2["x"]) / 2 + x_p, (v1['y'] + v2['y']) / 2 - y_p, text="D: " +
                                                                                                               obj[
                                                                                                                   'diameter'] + " мм" + "\n" + "L: " +
                                                                                                               obj[
                                                                                                                   'tp_lenth'] + " км"
                                                                                                               + "\n" + "G: " + str(
                        display_G),
                                            justify='right')
                    # self.canvas.create_text((v1["x"] + v2["x"]) / 2 + x_p, (v1['y'] + v2['y']) / 2 - y_p, text="D: " +
                    #                         obj['diameter'] + " мм" + "\n" + "L: " + obj['tp_lenth'] + " км"
                    #                         + "\n" + "G: " + obj['tp_G'] + " млн.т",
                    #                         justify='right')

    def add_object(self, **param):
        object_id = [i['id'] for i in self.objects if i['type'] == 'NPC' or i['type'] == 'NPC_RP']
        object_edge = [(i['npc1'], i['npc2']) for i in self.objects if i['type'] == 'tp']

        # добавление трубопровода NPC
        if self.radio1.get() == 0 and self.radio2.get() == 0:
            if param['id'] not in object_id:
                # self.objects.append({"id": str(param['id']), 'name': str(param['name']), 'type': 'NPC', "x": param['x'],
                #                      "y": param['y'], "lenghPoint": param['lenghPoint'], "param_a": param['param_a'],
                #                      "param_b": param['param_b'], "param_n": param['param_n'],
                #                      "param_t": param['param_t']
                #                      })
                self.objects.append({"id": str(param['id']), 'name': str(param['name']), 'type': 'NPC', "x": param['x'],
                                     "y": param['y'], "param_t": param['param_t']
                                     })
            else:
                messagebox.showinfo('Ошибка', 'Объект с таким именем уже существует!')

        # добавление трубопровода NPC_RP
        if self.radio1.get() == 1 and self.radio2.get() == 0:
            if param['id'] not in object_id:
                # self.objects.append({"id": param['id'], 'name': str(param['name']), 'type': 'NPC_RP', "x": param['x'],
                #                      "y": param['y'], "lenghPoint": param['lenghPoint'], "param_a": param['param_a'],
                #                      "param_b": param['param_b'], "param_n": param['param_n'],
                #                      "param_t": param['param_t'], 'parametrs': []})
                self.objects.append({"id": param['id'], 'name': str(param['name']), 'type': 'NPC_RP', "x": param['x'],
                                     "y": param['y'], "param_t": param['param_t'],
                                     'parametrs': []})
            else:
                messagebox.showinfo('Ошибка', 'НПС с таким именем уже существует!')

        if self.radio1.get() == 2 and self.radio2.get() == 0:
            per = self.inp_tp_first.get(), self.inp_tp_second.get()

            if per in object_edge:
                messagebox.showinfo("Задвоение объекта", "Трубопровод уже существует")
            elif self.inp_tp_first.get() not in object_id:
                messagebox.showinfo("404", "HПС 1 не найден.")
            elif self.inp_tp_second.get() not in object_id:
                messagebox.showinfo("404", "НПС 2 не найден.")
            elif self.inp_tp_first.get() in object_id and self.inp_tp_second.get() in object_id:
                self.objects.append({
                    "diameter": self.inp_tp_diameter.get(), 'type': 'tp', "npc1": self.inp_tp_first.get(),
                    "npc2": self.inp_tp_second.get(), 'tp_lenth': self.inp_tp_lenth.get(), 'tp_G': self.inp_tp_G.get()
                })

            else:
                messagebox.showerror("Ошибка", f"НПС не найдены!")

        self.canvas_update()

    def getnearestobject(self):
        d = 1000000
        res = {}
        for i in self.objects:
            # if self.browsed_object == i:
            #     continue

            if i['type'] == 'NPC' or i['type'] == 'NPC_RP':
                if sqr(self.X - i["x"]) + sqr(self.Y - i["y"]) < d:
                    d = sqr(self.X - i["x"]) + sqr(self.Y - i["y"])

                    self.browsed_object = i
                    if self.radio2.get() == 1:
                        self.updateParametrs()
                        self.inp_id.set(self.browsed_object['id'])
                        self.inp_name.set(self.browsed_object['name'])
                        # self.inp_lenghPoint.set(self.browsed_object['lenghPoint'])
                        # self.inp_param_a.set(self.browsed_object['param_a'])
                        # self.inp_param_b.set(self.browsed_object['param_b'])
                        # self.inp_param_n.set(self.browsed_object['param_n'])
                        self.inp_param_t.set(self.browsed_object['param_t'])

                        links = self.getObjLinksByTP(self.browsed_object['id'])
                        inputText = self.getObjLinksByTPString(links, 'input')
                        outputText = self.getObjLinksByTPString(links, 'output')

                        self.lb_inputs['text'] = "Вход: " + inputText
                        self.lb_outputs['text'] = "Выход: " + outputText

            # elif i['type'] == 'NPC_RP' and self.radio2.get() == 1:
            #     if sqr(self.X - i["x"]) + sqr(self.Y - i["y"]) < d:
            #         d = sqr(self.X - i["x"]) + sqr(self.Y - i["y"])
            #         self.browsed_object = i
            #         self.updateParametrs()
            #         self.inp_id.set(self.browsed_object['id'])
            #         self.inp_lenghPoint.set(self.browsed_object['lenghPoint'])

        if self.radio1.get() == 2:
            if self.browsed_object['type'] == 'NPC' or self.browsed_object['type'] == 'NPC_RP':
                if 'id' in self.browsed_object:
                    oldSelected1 = int(self.inp_tp_first.get())
                    oldSelected2 = int(self.inp_tp_second.get())
                    selected = int(self.browsed_object['id'])
                    if selected == oldSelected1 or oldSelected1 == 0:
                        if oldSelected2 != 0:
                            self.inp_tp_second.set(self.inp_tp_first.get())
                        self.inp_tp_first.set(int(self.browsed_object['id']))
                    else:
                        if oldSelected2 != 0:
                            self.inp_tp_first.set(self.inp_tp_second.get())
                        self.inp_tp_second.set(int(self.browsed_object['id']))
                    if self.radio2.get() == 1:
                        if selected != 0 and oldSelected1 != selected:
                            # self.browsed_object = i
                            self.updateParametrs()
                            tp = self.getTP(self.inp_tp_first.get(), self.inp_tp_second.get())
                            if tp:
                                self.browsed_object = tp
                                self.inp_tp_G.set(self.browsed_object['tp_G'])
                                self.inp_tp_lenth.set(self.browsed_object['tp_lenth'])
                                self.inp_tp_diameter.set(self.browsed_object['diameter'])
                # self.inp_tp_first.set(self.browsed_object['id'])

        self.canvas_update()

    def editobject(self):
        for i, obj in enumerate(self.objects):
            if self.radio1.get() <= 1:
                if obj['type'] == 'NPC':
                    if str(self.browsed_object['id']) == str(obj['id']):
                        self.objects[i] = {
                            "id": str(self.inp_id.get()),
                            "name": str(self.inp_name.get()),
                            # "param_a": str(self.inp_param_a.get()),
                            # "param_b": str(self.inp_param_b.get()),
                            # "param_n": str(self.inp_param_n.get()),
                            "param_t": str(self.inp_param_t.get()),
                            "type": 'NPC',
                            "x": obj["x"],
                            "y": obj["y"],
                            # "lenghPoint": self.inp_lenghPoint.get()
                        }

                if obj['type'] == 'NPC_RP':
                    if str(self.browsed_object['id']) == str(obj['id']):
                        self.objects[i] = {
                            "id": str(self.inp_id.get()),
                            "name": str(self.inp_name.get()),
                            # "param_a": str(self.inp_param_a.get()),
                            # "param_b": str(self.inp_param_b.get()),
                            # "param_n": str(self.inp_param_n.get()),
                            "param_t": str(self.inp_param_t.get()),
                            "type": 'NPC_RP',
                            "x": obj["x"],
                            "y": obj["y"],
                            "parametrs": self.objects[i]['parametrs'],
                            # "npc_q": str(self.inp_npc_q.get()),
                            # "npc_v": str(self.inp_npc_v.get()),
                            # "lenghPoint": self.inp_lenghPoint.get()
                        }

            if obj['type'] == 'tp' and self.radio1.get() == 2 and self.radio2.get() == 1:
                if obj['npc1'] == self.inp_tp_first.get() and obj['npc2'] == self.inp_tp_second.get():
                    self.objects[i] = {
                        "diameter": self.inp_tp_diameter.get(),
                        'type': 'tp',
                        "npc1": self.inp_tp_first.get(),
                        "npc2": self.inp_tp_second.get(),
                        'tp_lenth': self.inp_tp_lenth.get(),
                        'tp_G': self.inp_tp_G.get()
                    }

        self.canvas_update()

    def removeobject(self):
        fr = []
        edges = [i for i in self.objects if i['type'] == 'tp']

        if self.radio1.get() <= 1:
            if self.browsed_object in self.objects:
                self.objects.remove(self.browsed_object)
                for edge in edges:
                    if edge["npc1"] == self.browsed_object["id"] or edge["npc2"] == self.browsed_object["id"]:
                        fr.append(edge)
                for f in fr:
                    self.objects.remove(f)

        if self.radio1.get() == 2 and self.radio2.get() == 1:
            for edge in edges:
                if edge['npc1'] == self.inp_tp_first.get() and edge['npc2'] == self.inp_tp_second.get():
                    self.objects.remove(edge)

        self.canvas_update()

    def import_conf(self):
        path = askopenfilename(filetypes=[("Select file", "*.ini")])

        if path != '':
            self.objects.clear()

        with open(path, 'r') as file:
            self.objects = json.load(file)
            self.c = self.objects[0]['c']
            self.objects.remove(self.objects[0])

        self.canvas_update()

    def export_conf(self):
        path = asksaveasfilename(filetypes=[("Select file", "*.ini")])

        s = ''

        if ".ini" not in path:
            s = ".ini"

        with open(path + s, 'w') as file:
            self.objects.insert(0, {'c': self.c})
            json.dump(self.objects, file)

    def drop(self, e):
        if self.radio2.get() == 1 and self.radio1.get() <= 1:
            for i, obj in enumerate(self.objects):
                if obj == self.browsed_object:
                    self.objects[i]['x'] = e.x
                    self.objects[i]['y'] = e.y

        self.canvas_update()

    def motion(self, e):
        self.X, self.Y = e.x, e.y

    def clear(self):
        self.objects = []
        self.canvas_update()

    # сокрытие параметров в зависимости от объекта (трубопровод или НПС)
    def updateParametrs(self):
        if self.radio1.get() == 0:
            hide(
                self.lb_tp_length, self.lb_NPC1, self.lb_NPC2, self.tp_first, self.tp_second, self.btn_remove_object,
                self.btn_update_object, self.lb_diameter, self.tp_lenth, self.tp_diameter, self.tp_first,
                self.tp_second, self.btn_add_object, self.btn_add_param, self.lb_G, self.tp_G,
                self.btn_calc_Q, self.lb_Q, self.btn_calc_V, self.lb_V
            )

            # show(
            #     self.lb_id, self.lb_name, self.id, self.name, self.lb_len_point, self.npc_lenthPoint,
            #     self.lb_inputs, self.lb_outputs, self.lb_param_a, self.param_a, self.lb_param_b, self.param_b,
            #     self.lb_param_n, self.param_n, self.lb_param_t, self.param_t
            # )
            show(
                self.lb_id, self.lb_name, self.id, self.name,
                self.lb_inputs, self.lb_outputs, self.lb_param_t, self.param_t
            )

            if self.radio2.get() == 1:
                show(self.btn_update_object, self.btn_remove_object)

        elif self.radio1.get() == 1:
            hide(self.lb_tp_length, self.lb_NPC1, self.lb_NPC2, self.tp_first, self.tp_second, self.btn_remove_object,
                 self.btn_update_object, self.lb_diameter, self.tp_diameter, self.btn_add_object, self.tp_lenth,
                 self.btn_add_param, self.lb_G, self.tp_G, self.btn_calc_Q, self.lb_Q, self.btn_calc_V, self.lb_V
                 )

            # show(
            #     self.lb_id, self.lb_name, self.name, self.lb_len_point, self.id, self.npc_lenthPoint,
            #     self.lb_inputs, self.lb_outputs, self.lb_param_a, self.param_a, self.lb_param_b, self.param_b,
            #     self.lb_param_n, self.param_n, self.lb_param_t, self.param_t
            # )
            show(
                self.lb_id, self.lb_name, self.name,
                self.lb_inputs, self.lb_outputs, self.lb_param_t, self.param_t
            )

            if self.radio2.get() == 1:
                show(self.btn_remove_object, self.btn_update_object, self.btn_add_param)

        elif self.radio1.get() == 2:
            # hide(self.lb_id, self.lb_name, self.name, self.lb_NPC1, self.lb_NPC2, self.lb_len_point,
            #      self.npc_lenthPoint,
            #      self.btn_update_object, self.btn_add_param, self.btn_remove_object, self.btn_add_param,
            #      self.lb_inputs, self.lb_outputs,
            #      self.lb_param_a, self.param_a, self.lb_param_b, self.param_b, self.lb_param_n, self.param_n,
            #      self.lb_param_t, self.param_t, self.btn_calc_Q, self.lb_Q, self.btn_calc_V, self.lb_V)
            hide(self.lb_id, self.lb_name, self.name, self.lb_NPC1, self.lb_NPC2,
                 self.btn_update_object, self.btn_add_param, self.btn_remove_object, self.btn_add_param,
                 self.lb_inputs, self.lb_outputs,
                 self.lb_param_t, self.param_t, self.btn_calc_Q, self.lb_Q, self.btn_calc_V, self.lb_V)

            show(self.tp_first, self.tp_second, self.lb_NPC1, self.lb_NPC2, self.lb_tp_length, self.lb_diameter,
                 self.tp_diameter, self.btn_add_object, self.tp_lenth, self.lb_G, self.tp_G,
                 )

            if self.radio2.get() == 1:
                show(self.btn_remove_object, self.btn_update_object, self.tp_lenth, self.btn_calc_Q, self.lb_Q,
                     self.btn_calc_V, self.lb_V)

    # 2. Убрать ошибку в счете индексов при добавлении новых элементов
    # максимальное имя объекта
    def getMaxId(self):
        maxname = 0
        for obj in self.objects:
            # если есть свойство 'id' у объекта
            if 'id' in obj:
                # преобразуем в число и сравниваем с максимальным
                intname = int(obj['id'])
                if intname > maxname:
                    # если больше максимального - устанавливаем как максимальное
                    maxname = intname
        # устанавливаем для нового добавляемого объекта имя как максимальное + 1
        return str(maxname + 1)

    def getObj(self, id):
        for obj in self.objects:
            if 'id' in obj:
                if obj['id'] == id:
                    return obj

    def getObjName(self, obj):
        objname = "НПС" + obj['id']
        if obj['name']:
            objname = obj['name']
        return objname

    def getTP(self, npc1, npc2):
        for obj in self.objects:
            if 'npc1' in obj and 'npc2' in obj:
                if obj['npc1'] == npc1 and obj['npc2'] == npc2:
                    return obj
        return None

    def getObjInputByTPs(self, id):
        result = []
        obj = self.getObj(id)
        if obj:
            tpInputs = self.getObjLinksByTP(id, 'input')
            for tpInput in tpInputs:
                tpInputOutputs = self.getObjOutputByTPs(tpInput['obj']['id'])
                for tpInputOutput in tpInputOutputs:
                    if tpInputOutput['to'] == id:
                        result.append(tpInputOutput)
        return result

    def getObjOutputByTPs(self, id):
        result = []
        obj = self.getObj(id)
        if obj:
            objLinks = self.getObjLinksByTP(id, 'output')
            # tpCount = len(objLinks)
            # for n, obj in enumerate(obj['parametrs']):
            #     if n < tpCount:
            #         result.append({"from": id, "to": str(objLinks[n]['obj']['id']), "v": obj[0], "q": obj[1]})
            for obj_link in objLinks:
                q, v = 0, 0
                if 'input_qv' in obj_link['obj']:
                    if 'q' in obj_link['obj']['input_qv']:
                        q = obj_link['obj']['input_qv']['q']
                    if 'v' in obj_link['obj']['input_qv']:
                        v = obj_link['obj']['input_qv']['v']
                result.append({"from": id, "to": str(obj_link['obj']['id']), "v": v, "q": q})
        return result

    def getObjLinksByTP(self, id, filter=''):
        result = []
        for obj in self.objects:
            if 'npc1' in obj and 'npc2' in obj:
                if obj['npc1'] == id and (filter == '' or filter == 'output'):
                    outObj = self.getObj(obj['npc2'])
                    if outObj:
                        result.append({"type": 'output', "obj": outObj, "name": self.getObjName(outObj)})
                elif obj['npc2'] == id and (filter == '' or filter == 'input'):
                    inpObj = self.getObj(obj['npc1'])
                    if inpObj:
                        result.append({"type": 'input', "obj": inpObj, "name": self.getObjName(inpObj)})
        return result

    def getObjLinksByTPString(self, links, type):
        counter = 0
        result = ""
        for line in links:
            if line['type'] == type:
                if counter > 0:
                    result = result + ", "
                result = result + line['name']
                counter = counter + 1
        if counter > 0:
            result = " " + str(counter) + " от " + result
        return result

    def click(self, e):

        # Добавление
        if self.radio2.get() == 0:
            # НПС
            if self.radio1.get() == 0:

                self.inp_id.set(self.getMaxId())
                # self.add_object(id=self.inp_id.get(), name=self.inp_name.get(), x=e.x, y=e.y,
                #                 lenghPoint=self.inp_lenghPoint.get(), param_a=self.inp_param_a.get(),
                #                 param_b=self.inp_param_b.get(), param_n=self.inp_param_n.get(),
                #                 param_t=self.inp_param_t.get())
                self.add_object(id=self.inp_id.get(), name=self.inp_name.get(), x=e.x, y=e.y,
                                param_t=self.inp_param_t.get())

            # НПС с резервуарным баком
            elif self.radio1.get() == 1:
                self.inp_id.set(self.getMaxId())
                # self.add_object(id=self.inp_id.get(), name=self.inp_name.get(), x=e.x, y=e.y,
                #                 lenghPoint=self.inp_lenghPoint.get(), param_a=self.inp_param_a.get(),
                #                 param_b=self.inp_param_b.get(), param_n=self.inp_param_n.get(),
                #                 param_t=self.inp_param_t.get())
                self.add_object(id=self.inp_id.get(), name=self.inp_name.get(), x=e.x, y=e.y,
                                param_t=self.inp_param_t.get())

            # Трубопровод
            elif self.radio1.get() == 2:
                self.getnearestobject()

        elif self.radio2.get() == 1:
            self.getnearestobject()

        try:
            self.param_win.destroy()
        except:
            pass

        self.canvas_update()


if __name__ == '__main__':
    window = Tk()
    mywin = MyWindow(window)
    window.title("Схема системы нефтепровода")
    window.geometry("1145x628")

    window.resizable(width=False, height=False)
    window.mainloop()