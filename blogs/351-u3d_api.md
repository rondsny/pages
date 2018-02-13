title: "[Unity]Unity常见API"
date: 2017-05-04 14:06:44 
tags: unity,u3d
---

## Unity常见API

本文主要为了方便查阅

### 1. MonoBehaviour 生命周期

- Awake 对象创建的时候调用，类似构造函数
- Start 在`Awake`之后执行，区别在于，如果组件不可用（在`Inspector`没有勾选该组件），是不会执行`Start`的
- Update 主函数循环每帧调用
- FixedUpdate 每次固定帧调用，在物理计算的时候，应该使用该方法，而不是`Update`
- OnDestroy 对象销毁时调用

### 2. MonoBehaviour 常见回调函数

- OnMouseEnter 鼠标移入GUI控件或者碰撞体时调用
- OnMouseOver 鼠标停留在GUI控件或者碰撞体时调用
- OnMouseExit 鼠标移出GUI控件或者碰撞体时调用
- OnMouseDown 鼠标在GUI控件或者碰撞体上按下时调用
- OnMouseUp 鼠标在GUI控件或者碰撞体上释放时调用
- OnTriggerEnter 当其他碰撞体进入触发器时调用
- OnTriggerExit 当其他碰撞体离开触发器时调用
- OnCollisionEnter 当碰撞体或者刚体与其他碰撞体或刚体接触时调用
    - OnCollisionEnter2D 其它2D函数类似
- OnCollisionExit 当碰撞体或者刚体与其他碰撞体或刚体停止接触时调用
- OnCollisionStay 当碰撞体或者刚体与其他碰撞体或刚体保持接触时调用
- OnContollerColliderHit 当控制器移动时与碰撞体发生碰撞时调用
- OnBecameVisible 对于任意一个相机可见时调用
- OnBecameInVisible 对于任意一个相机不可见时调用
- OnEnable 对象启用或者激活时调用
- OnDisable 对象禁用或者取消激活时调用
- OnDestroy 脚本销毁时调用
- OnGUI 渲染GUI和处理GUI消息时调用


### 3. 访问游戏对象

- GameObject.Find 多个时返回第一个
- GameObject.FindWithTag 多个时返回第一个
- GameObject.FindGameObjectsWithTag 返回数组

以上函数比较耗时，尽量避免在update函数中使用。

### 4. 访问组件 

#### 4.1. 常见组件

- Transform 位置、旋转、缩放
- Rigidbody 刚体
- Renderer 渲染物体模型
- Light 灯光属性
- Camera 相机属性
- Collider 碰撞体
- Animation 动画
- Audio 声音
- Mesh
    - Mesh Filter 网格过滤器
    - Text Mesh 文本
    - Mesh Renderer 网格渲染器
    - Skinned Mesh Renderer 蒙皮渲染器，用于骨骼动画
- Particle Sysyem 粒子系统
- Physics 物理
- Image Effects
- Scripts 自定义组件

#### 4.2. 获取组件

- GetComponent<>() 获取组件
- GetComponents<>()
- GetComponentInChildren<>() 得到对象或者对象子物体上的组件
- GetComponentsInChildren<>()

以上函数比较耗时，尽量避免在update函数中使用。

#### 4.3. Transform 组件

##### 4.3.1. 成员变量

- position 世界坐标系
- localPosition 相对坐标系(父对象)
- eulerAngles 世界坐标系中以欧拉角表示的旋转
- localEulerAngles 相对旋转
- right 右方向
- up 上方向
- forward 前方向
- rotation 旋转四元数
- localRotation 相对旋转四元数
- localScale 相对缩放比例
- parent 父对象的Transform组件
- worldToLocalMatrix 世界坐标系到局部坐标系的变换矩阵(只读)
- localToWorldMatrix 局部坐标系到世界坐标系的变换矩阵(只读)
- root 根对象的Transform组件
- childCount 子孙对象的数量
- lossyScale 全局缩放比例(只读)

##### 4.3.2. 成员函数

- Translate 按指定方向和距离平移
- Rotate 按指定的欧拉角旋转
- RotateAround 按给定旋转轴和旋转角度进行旋转
- LookAt 旋转使得自身的前方向指向目标的位置
- TransformDirection 将一个方向从局部坐标系变换到世界坐标系
- InverseTansformDirection 将一个方向从世界坐标系变化到局部坐标系
- DetachChildren 与所有子物体接触父子关系
- Find 按名称查找子对象
- IsChildOf 判断是否是指定对象的子对象

### 5. Time 时间类

#### 5.1. 成员变量

- time 游戏从开始到现在经历的时间(秒)(只读)
- timeSinceLevelLoad 此帧开始时间(秒)(只读)，从关卡加载完成开始计算
- dateTime 上一帧耗费的时间(秒)(只读)
- fixedTime 最近FixedUpdate的时间。该时间从游戏开始计算
- fixedDateTime 物理引擎和FixedUpdate的更新时间间隔
- maximunDateTime 一帧的最大耗时时间
- smoothDeltaTime Time.deltaTime的平滑淡出
- timeScale 时间流逝速度的比例。可以制作慢动作特效
- frameCount 已渲染的帧的总数(只读)
- realtimeSinceStartup 游戏从开始到现在的真实时间(秒)，该事件不受timeScale影响
- captureFramerate 固定帧率设置

### 6. Random 随机数类

#### 6.1. 成员变量

- seed 随机数生成器种子
- value 0~1随机数，包含0和1
- insideUnitSphere 半径为1的球体内的一个随机点
- insideUnitCircle 半径为1的圆内的一个随机点
- onUnitSphere 半径为1的球面上的一个随机点
- rotation 随机旋转
- rotationUnitform 均匀分布的随机旋转

#### 6.2. 成员函数

- Range 返回(min,max)直接的随机浮点数，包含min和max


### 7. Mathf 数学类

#### 7.1. 成员变量

- PI
- Infinity 正无穷大
- NegativeInfinity 负无穷大
- Deg2Rad 度到弧度的转换系数
- Rad2Deg 弧度到度的转换系数
- Epsilon 一个很小的浮点数

#### 7.2. 成员函数

- Sin 弧度
- Cos 弧度
- Tan 弧度
- Asin 角度
- ACos 角度
- Atan 角度
- Sqrt 计算平方根
- Abs 绝对值
- Min
- Max
- Pow Pow(f,p) f的p次方
- Exp Exp(p) e的p次方
- Log 计算对数
- Log10 计算基为10的对数
- Ceil 向上取整
- Floor 向下取整
- Round 四舍五入
- Clamp 将数值限制在min和max之间
- Clamp01 将数值限制在0和1之间

### 8. Coroutine 协同程序函数

- StartCoroutine 启动一个协同程序
- StopCoroutine 终止一个协同程序
- StopAllCoroutines 终止所有协同程序
- WaitForSeconds 等到若干秒
- WaitForFixedUpdates 等待直到下一次FiexedUpdate调用