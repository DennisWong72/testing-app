import time, random

class IdleGame:

    attr_init = [100, 0]
    attr_step = 1.03
    hit_init = [100, 0]
    attr_name = ['power', 'magic', 'sword', 'speed', 'punch']
    hit_key = 'hit'

    enemy_key = 'enemy'
    enemy_init = [115, 0]
    enemy_step = pow(attr_step, len(attr_name)) # 1.159274

    asset_key = 'asset_sec'
    asset_init = [1, 0]
    asset_step = 1.1
    assetall_key = 'asset_all'

    elem = {}

    def __init__(self):
        self.attr_initial()

    def fix_val(self, a):
        while a[0] > 1000:
            a[0] /= 10
            a[1] += 1
        while a[0] < 100 and a[1] > 0:
            a[0] *= 10
            a[1] -= 1

    def op_val(self, a, b, op):
        if op == '+=':
            a[0] += b[0]*pow(10, b[1]-a[1])
            self.fix_val(a)
        elif op == '-=':
            a[0] -= b[0]*pow(10, b[1]-a[1])
            self.fix_val(a)
        elif op == '>=':
            c = a[1]*1000 + a[0]
            d = b[1]*1000 + b[0]
            return c >= d
        else:
            raise Exception('op_val error')
        return 0    

    def attr_initial(self):
        for key in self.attr_name:
            self.elem[key] = self.attr_init.copy()
            self.elem[key+'lv'] = 1

            self.elem[key+'costday'] = [24*60*60*self.asset_init[0]*pow(10, self.asset_init[1])/len(self.attr_name), 0]
            self.fix_val(self.elem[key+'costday'])
            
            self.elem[key+'cost'] = [100, 0]
        self.elem[self.hit_key] = self.hit_init.copy()

        self.elem[self.enemy_key] = self.enemy_init.copy()
        self.elem[self.enemy_key+'lv'] = 1
        self.elem[self.asset_key] = self.asset_init.copy()

        self.elem[self.assetall_key] = [0, 0]

    def attr_up_self(self, key):
        valid_key = self.attr_name + [self.hit_key, self.enemy_key, self.asset_key]
        valid_key += [x+'costday' for x in self.attr_name]
        if key not in valid_key:
            raise Exception('key error in attr_up_self()')

        a = self.elem[key]

        if key == self.enemy_key:
            step = self.enemy_step
        elif key == self.asset_key or 'costday' in key:
            step = self.asset_step
        else: # key == hit_key or key in self.attr_name
            step = self.attr_step

        a[0] *= step
        self.fix_val(a)

    def attr_lvup(self, key):
        valid_key = self.attr_name + [self.enemy_key]
        if key not in valid_key:
            raise Exception('key error in attr_lvup()')

        self.elem[key+'lv'] += 1
        self.attr_up_self(key)

        if key == self.enemy_key:
            self.attr_up_self(self.asset_key)
        else: #if key in self.attr_name:
            self.attr_up_self(self.hit_key)
            self.attr_up_self(key+'costday')
            self.update_attr_cost(key)

    def update_attr_cost(self, key):
        # before call this, update lv, costday of attr first
        valid_key = self.attr_name
        if key not in valid_key:
            raise Exception('key error in update_attr_cost()')
        
        rate_tb = [(30,0.006), (60,0.1), (100,0.3)]

        lv = self.elem[key+'lv']
        if lv <= rate_tb[0][0]:
            costday_rate = rate_tb[0][1]
        elif lv >= rate_tb[-1][0]:
            costday_rate = rate_tb[-1][1]
        else:
            for idx in range(len(rate_tb)):
                if lv <= rate_tb[idx+1][0]:
                    a = rate_tb[idx]
                    b = rate_tb[idx+1]
                    costday_rate = a[1]+((b[1]-a[1])/(b[0]-a[0]))*(lv-a[0])
                    break
        a = self.elem[key+'cost'] 
        b = self.elem[key+'costday']
        a[0] = b[0]*costday_rate
        a[1] = b[1]
        self.fix_val(a)

    def get_attr_str(self, key):
        a = self.elem[key]
        if a[1] == 0:
            return f'{a[0]:.0f}'
        return f'{a[0]:.0f}*10^{a[1]}'

    def print_elem(self):
        for key in self.attr_name:
            print('%s: Lv %d, %s, UpCost %s' % (key.capitalize(), self.elem[key+'lv'], self.get_attr_str(key), self.get_attr_str(key+'cost')))
        print('%s = %s' % (self.hit_key.capitalize(), self.get_attr_str(self.hit_key)))
        print('%s: Lv %d, %s' % (self.enemy_key.capitalize(), self.elem[self.enemy_key+'lv'], self.get_attr_str(self.enemy_key)))
        print('%s = %s, %s = %s' % (self.assetall_key.capitalize(), self.get_attr_str(self.assetall_key), 
                                    self.asset_key.capitalize(), self.get_attr_str(self.asset_key)))
        print('='*30)

    def check_beat_enemy(self):
        a = self.elem[self.hit_key]
        b = self.elem[self.enemy_key]
        return self.op_val(a, b, '>=')
    
    def per_sec_auto_play(self):
        a = self.elem[self.assetall_key]
        b = self.elem[self.asset_key]
        self.op_val(a, b, '+=')

        # random to check if we can up
        key = random.choice(self.attr_name)
        c = self.elem[key+'cost']
        if self.op_val(a, c, '>='):
            self.op_val(a, c, '-=')
            self.attr_lvup(key)
            if self.check_beat_enemy():
                self.attr_lvup(self.enemy_key)
            #self.print_elem()

if __name__ == '__main__':
    game = IdleGame()
    
    for day in range(30):
        for idx in range(24*60*60):
            game.per_sec_auto_play()
        game.print_elem()