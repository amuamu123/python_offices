import matplotlib.pylab as plt  # python图形可视化库
import numpy as np  # 科学计算库
from mpl_toolkits.mplot3d import Axes3D # 3d绘图


def draw_scatter():
    """单独画散点图"""
    N = 30  # 扩大到每组30个点
    scatter_x1, scatter_y1, scatter_x2, scatter_y2, scatter_scatter_x3, scatter_y3 = \
        [np.random.rand(N) * 100 for i in range(6)]  # 每组15个0-15的随机数
    plt.scatter(scatter_x1, scatter_y1, c='r', s=100, alpha=0.5)  # c颜色，s大小，alpha透明度
    plt.scatter(scatter_x2, scatter_y2, c='g', s=200, alpha=0.5)
    plt.scatter(scatter_scatter_x3, scatter_y3, c='b', s=300, alpha=0.5)
    # plt.legend(loc='upper right', labels=['medium', 'small', "big"])
    plt.title("scatter")
    plt.show()


def draw_3d_scatter():
    """3d散点图"""
    data = np.random.randint(0, 255, size=[40, 40, 40])
    x, y, z = data[0], data[1], data[2]
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    #  将数据点分成三部分画，在颜色上有区分度
    ax.scatter(x[:10], y[:10], z[:10], c='y')  # 绘制数据点
    ax.scatter(x[10:20], y[10:20], z[10:20], c='r')
    ax.scatter(x[30:40], y[30:40], z[30:40], c='g')
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()


def draw_bar():
    """单独画柱状图"""
    n = 12
    bar_x = np.arange(n)
    # 均匀分布
    bar_y1 = (1 - bar_x / float(n)) * np.random.uniform(0.5, 1.0, n)
    bar_y2 = (1 - bar_x / float(n)) * np.random.uniform(0.5, 1.0, n)

    plt.bar(bar_x, +bar_y1, facecolor='#9999ff', edgecolor='white')  #填充颜色， 和边框颜色
    plt.bar(bar_x, -bar_y2, facecolor='#ff9999', edgecolor='white')
    plt.xlim(-1, n)
    plt.xticks(())  # x轴刻度 默认设置
    plt.ylim(-1.25, 1.25)  # 纵坐标的刻度范围
    plt.yticks(())

    for x, y in zip(bar_x, bar_y1):
        #ha: horizontal alignment 水平对齐
        #va: vertical alignment  垂直对齐
        #y+0.05， 文字的向上偏移度
        plt.text(x, y + 0.05, '%.2f' % y, ha='center', va='bottom')

    for x, y in zip(bar_x, bar_y2):
        plt.text(x, -y - 0.05, '%.2f' % y, ha='center', va='top')
    plt.legend(loc='upper right', labels=['up', 'down'])
    plt.title("bar")
    plt.show()


def draw_pie():
    """单独画饼图"""
    labels = 'c', 'python', 'java', 'c++'
    sizes = 15, 30, 35, 10
    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral'
    explode = 0, 0.1, 0, 0  #第二个元素偏离圆心 0.1
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=50)
    plt.axis('equal')
    plt.title("pie")
    plt.show()


def draw_doughnut():
    """圆环图"""
    labels = 'c', 'python', 'java', 'c++'
    sizes = 15, 30, 35, 10
    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral'
    # explode = 0, 0.1, 0, 0  #第二个元素偏离圆心 0.1
    plt.pie(sizes, wedgeprops=dict(width=0.3,edgecolor='w'), labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=50)
    plt.axis('equal')
    plt.title("doughnut")
    plt.show()


def draw_love_curve():
    """单独画笛卡尔爱心曲线"""
    t = np.arange(0, 2 * np.pi, 0.1)
    # 参数方程
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    plt.plot(x, y, color='red')
    plt.title("love_curve")
    plt.fill_between(x, y, facecolor='pink')
    plt.show()


def draw_line_chart():
    """单独画折线图"""
    x = np.arange(9)
    y = np.sin(x)
    z = np.cos(x)
    plt.plot(x, y, marker="*", linewidth=3, linestyle="--", color="orange")
    plt.plot(x, z)
    plt.title("line_chart")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(["Y","Z"], loc="upper right")
    plt.grid(True)
    plt.show()


def draw_3d_hookface():
    """单独画3d曲面图"""
    figure = plt.figure()
    ax = Axes3D(figure)
    X = np.arange(-4, 4, 0.25)
    Y = np.arange(-4, 4, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap='rainbow')
    plt.show()


if __name__ == "__main__":
    draw_bar()
    draw_scatter()
    draw_3d_scatter()
    draw_pie()
    draw_doughnut()
    draw_love_curve()
    draw_line_chart()
    draw_3d_hookface()#3d曲面图