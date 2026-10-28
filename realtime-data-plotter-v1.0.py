import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

try:
    # 务必确认端口是 COM3，且 Arduino 串口监视器已关闭！
    ser = serial.Serial('COM3', 9600, timeout=1)
    ser.reset_input_buffer() 
except Exception as e:
    print(f"串口打开失败: {e}")
    exit()

fig, ax = plt.subplots()
ax.set_ylim(0, 1050)
ax.set_xlim(0, 100)
ax.set_title("FSR404 Real-time Pressure Monitor")
ax.set_ylabel("Weight / Force (g)")
ax.grid(True)

# 初始数据
y_data = [0] * 100
x_data = list(range(100))

# 初始化曲线
line, = ax.plot(x_data, y_data, color='blue', linewidth=2)

def update(frame):
    global y_data
    # 只要缓冲区有数据，就把所有堆积的数据读完，防止画面延迟
    while ser.in_waiting > 0:
        try:
            raw_data = ser.readline().decode('utf-8').strip()
            if raw_data:
                print(f"收到原始数据: {raw_data}") # 终端打印调试
                value = float(raw_data)
                y_data.pop(0)
                y_data.append(value)
        except ValueError as e:
            print(f"转换错误: {e}")

    # 关键修复：显式地将一维列表转换为标准的线条坐标，避免广播冲突
    line.set_xdata(x_data)
    line.set_ydata(y_data)
    return line,

# 关键修复：加入 cache_frame_data=False，彻底关掉 matplotlib 内部的帧缓存和冲突检测
ani = animation.FuncAnimation(fig, update, interval=50, blit=True, cache_frame_data=False)
plt.show()
