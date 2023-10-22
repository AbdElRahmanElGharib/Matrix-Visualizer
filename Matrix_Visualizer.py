# import needed libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation as anim, markers
from IPython.display import HTML
import os

# class definition 
class Matrix_Visualizer:
    
    def __init__(self, a = 1, b = 0, c = 0, d = 1):
        
        self._initial_state = None
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        
        self._fig = plt.figure(figsize=(16,9), dpi=240)
        self._ax= plt.subplot(1,1,1)
        self._ax.set_facecolor('black')

        self._ax.set_xlim(( -8, 8))
        self._ax.set_ylim((-4.5, 4.5))
        
        for i in range(-10, 10):
            self._ax.plot([-100,100], [i,i], '#263142', lw=0.75)
            self._ax.plot([i,i], [-100,100], '#263142', lw=0.75)
        
        self._ax.plot([-100,100], [0,0], '#586c79', lw=1.5)
        self._ax.plot([0,0], [-100,100], '#586c79', lw=1.5)
         
        self._x_axis_limits = [[-100,0],
                              [100,0]]
        self._x_axis, =    self._ax.plot([self._x_axis_limits[0][0],self._x_axis_limits[1][0]],
                                       [self._x_axis_limits[0][1],self._x_axis_limits[1][1]],
                                       '#87cbf5', lw=2)
        self._y_axis_limits = [[0,-100],
                              [0,100]]
        self._y_axis, =    self._ax.plot([self._y_axis_limits[0][0],self._y_axis_limits[1][0]],
                                       [self._y_axis_limits[0][1],self._y_axis_limits[1][1]],
                                       '#87cbf5', lw=2)

        self._grid_lines_h = []
        self._grid_lines_h_limits = []
        self._grid_lines_v = []
        self._grid_lines_v_limits = []

        self._fine_grid_lines_h = []
        self._fine_grid_lines_h_limits = []
        self._fine_grid_lines_v = []
        self._fine_grid_lines_v_limits = []

        for x in range(-50,51):
            if x == 0:
                continue
            self._grid_lines_v_limits.append([[x,-100],
                                             [x,100]])
            self._grid_lines_v.append(*self._ax.plot([self._grid_lines_v_limits[-1][0][0],self._grid_lines_v_limits[-1][1][0]],
                                                  [self._grid_lines_v_limits[-1][0][1],self._grid_lines_v_limits[-1][1][1]],
                                                  '#316ac4', lw=1))

        for y in range(-50,51):
            if y == 0:
                continue
            self._grid_lines_h_limits.append([[-100,y],
                                             [100,y]])
            self._grid_lines_h.append(*self._ax.plot([self._grid_lines_h_limits[-1][0][0],self._grid_lines_h_limits[-1][1][0]],
                                                  [self._grid_lines_h_limits[-1][0][1],self._grid_lines_h_limits[-1][1][1]],
                                                  '#316ac4', lw=1))
            
        for x in range(-50,51):
            self._fine_grid_lines_v_limits.append([[x+0.5,-100],
                                                  [x+0.5,100]])
            self._fine_grid_lines_v.append(*self._ax.plot([self._fine_grid_lines_v_limits[-1][0][0],self._fine_grid_lines_v_limits[-1][1][0]],
                                                       [self._fine_grid_lines_v_limits[-1][0][1],self._fine_grid_lines_v_limits[-1][1][1]],
                                                       '#092787', lw=0.5))
            
        for y in range(-50,51):
            self._fine_grid_lines_h_limits.append([[-100,y+0.5],
                                                  [100,y+0.5]])
            self._fine_grid_lines_h.append(*self._ax.plot([self._fine_grid_lines_h_limits[-1][0][0],self._fine_grid_lines_h_limits[-1][1][0]],
                                                       [self._fine_grid_lines_h_limits[-1][0][1],self._fine_grid_lines_h_limits[-1][1][1]],
                                                       '#092787', lw=0.5))
        
    def set_matrix(self, a,b,c,d):
        
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        
        self.get_matrix()
        
    def get_matrix(self):
        
        matrix = [[self._a,self._b],
                  [self._c,self._d]]
        print('The Matrix is set to:\t', matrix)
    
    def _get_new_x(self, old_x, old_y):
        return (self._a*old_x + self._b*old_y)
    
    def _get_new_y(self, old_x, old_y):
        return (self._c*old_x + self._d*old_y)
    
    def _new_xy(self, pos):
        old_x, old_y = pos[0], pos[1]
        return [self._get_new_x(old_x=old_x, old_y=old_y), self._get_new_y(old_x=old_x, old_y=old_y)]
    
    def _new_limits(self, line_old_limits):
        return [self._new_xy(line_old_limits[0]), self._new_xy(line_old_limits[1])]
    
    def _new_limits_group(self, old):
        new_limits = []
        for sublist in old:
            new_limits.append(self._new_limits(sublist))
        return new_limits
    
    def _update(self):
        self._x_axis.set_data([self._x_axis_limits[0][0],self._x_axis_limits[1][0]],
                             [self._x_axis_limits[0][1],self._x_axis_limits[1][1]])
        self._y_axis.set_data([self._y_axis_limits[0][0],self._y_axis_limits[1][0]],
                             [self._y_axis_limits[0][1],self._y_axis_limits[1][1]])
        
        for line, line_limits in zip(self._grid_lines_h, self._grid_lines_h_limits):
            line.set_data([line_limits[0][0],line_limits[1][0]],
                          [line_limits[0][1],line_limits[1][1]])
        
        for line, line_limits in zip(self._grid_lines_v, self._grid_lines_v_limits):
            line.set_data([line_limits[0][0],line_limits[1][0]],
                          [line_limits[0][1],line_limits[1][1]])
        
        for line, line_limits in zip(self._fine_grid_lines_h, self._fine_grid_lines_h_limits):
            line.set_data([line_limits[0][0],line_limits[1][0]],
                          [line_limits[0][1],line_limits[1][1]])
        
        for line, line_limits in zip(self._fine_grid_lines_v, self._fine_grid_lines_v_limits):
            line.set_data([line_limits[0][0],line_limits[1][0]],
                          [line_limits[0][1],line_limits[1][1]])
    
    def _update_limits(self, new_state):
        self._x_axis_limits = new_state[0]
        self._y_axis_limits = new_state[1]
        self._grid_lines_h_limits = new_state[2]
        self._grid_lines_v_limits = new_state[3]
        self._fine_grid_lines_h_limits = new_state[4]
        self._fine_grid_lines_v_limits = new_state[5]
    
    def _get_final_state_limits(self):
        x_axis = self._new_limits(self._x_axis_limits)
        y_axis = self._new_limits(self._y_axis_limits)
        grid_h = self._new_limits_group(self._grid_lines_h_limits)
        grid_v = self._new_limits_group(self._grid_lines_v_limits)
        gridfh = self._new_limits_group(self._fine_grid_lines_h_limits)
        gridfv = self._new_limits_group(self._fine_grid_lines_v_limits)
        
        return [x_axis,
                y_axis,
                grid_h,
                grid_v,
                gridfh,
                gridfv]
    
    def _animate(self) -> anim.FuncAnimation:
        
        self._initial_state = [self._x_axis_limits,
                         self._y_axis_limits,
                         self._grid_lines_h_limits,
                         self._grid_lines_v_limits,
                         self._fine_grid_lines_h_limits,
                         self._fine_grid_lines_v_limits]
        
        self._final_state = self._get_final_state_limits()
        
        def drawframe(n):
            if n < 16 or n > 102:
                return tuple()
            
            state = self._get_state(n)
            
            self._update_limits(state)
            self._update()
            return (self._x_axis,
                    self._y_axis,
                    *self._grid_lines_h,
                    *self._grid_lines_v,
                    *self._fine_grid_lines_h,
                    *self._fine_grid_lines_v)

        animation = anim.FuncAnimation(self._fig, drawframe, frames=120, interval=16, blit=True)

        return animation
    
    def get_html_animation(self):
        animation = self._animate()
        return HTML(animation.to_html5_video())
    
    def save_animation(self, name = 'animation.mp4'):
        
        animation = self._animate()
        animation.save(filename = name)
        return self
        
    def play(self):
        if self._initial_state == None:
            print('Animation is not made yet. Call save_animation() first.')
            return
        os.system(command=r'cmd /c ""C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe" "C:\Users\AbdElRahman_ElGharib\Desktop\a\animation.mp4""')

    def _get_state(self, n):
        state = []
        for i in range(6):
            state.append(((np.array(self._final_state[i]) - np.array(self._initial_state[i])) / 86 * (n-16)) + np.array(self._initial_state[i]))
        return state
    
# main program
if __name__ == '__main__':
    while True:
        print('''The matrix is in the formula [[A, B],
                              [C, D]]''')
        a = int(input('Enter [A] value then press [Enter]:\t'))
        b = int(input('Enter [B] value then press [Enter]:\t'))
        c = int(input('Enter [C] value then press [Enter]:\t'))
        d = int(input('Enter [D] value then press [Enter]:\t'))
        Matrix_Visualizer(a,b,c,d)\
            .save_animation()\
            .play()
        query = input('do you want to see another animation:\t\t[y]/[n]\n').strip().lower()
        if query == 'n':
            break
