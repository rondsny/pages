title: "[Bullet3]三种碰撞检测及实现"
date: 2017-02-16 21:56:57
tags: Bullet3
---

官方文档：http://bulletphysics.org
开源代码：https://github.com/bulletphysics/bullet3/releases
API文档：http://bulletphysics.org/Bullet/BulletFull/annotated.html

## bullet3的三种碰撞检测

以下三种方式都是可以达到碰撞检测的效果：

1. `btCollisionWorld::contactTest` 检测指定对象是否与场景发生碰撞；
2. `btCollisionWorld::performDiscreteCollisionDetection` 检测场景中所有的碰撞；
3. `btDynamicsWorld::stepSimulation` 模拟运动。

还有一种射线检测，但是与这里的物体碰撞稍微有些区别，这里就不展开来讲了。

### 0. 准备工作

先创建一个场景，增加一个地板（box）

```cpp
btDefaultCollisionConfiguration* g_colConfig;
btCollisionDispatcher* g_dispatcher;
btBroadphaseInterface* g_broadInterface;
btSequentialImpulseConstraintSolver* g_solver;
btDynamicsWorld* g_world;  // 场景信息，退出的时候需要delete

g_colConfig = new btDefaultCollisionConfiguration();
g_dispatcher = new btCollisionDispatcher(g_colConfig);
g_broadInterface = new btDbvtBroadphase();
g_solver = new btSequentialImpulseConstraintSolver;
g_world = new btDiscreteDynamicsWorld(g_dispatcher, g_broadInterface, g_solver, g_colConfig);

g_world->setGravity(btVector3(0,-10,0));      // 设置重力加速度

// add a test box
{
    btCollisionShape* shape = new btBoxShape(btVector3(btScalar(1000.),btScalar(10.),btScalar(1000.)));
    btTransform trans;
    trans.setIdentity();
    trans.setOrigin(btVector3(0, -10, 0));

    btScalar mass=0.f;
    btVector3 localInertia(0, 0, 0);
    bool isDynamic = (mass != 0.f);
    if (isDynamic)
        shape->calculateLocalInertia(mass, localInertia);

    btDefaultMotionState* myMotionState = new btDefaultMotionState(trans);
    btRigidBody::btRigidBodyConstructionInfo cInfo(mass, myMotionState, shape, localInertia);
    btRigidBody* body = new btRigidBody(cInfo);
    g_world->addRigidBody(body);
}
```

### 1. `btCollisionWorld::contactTest`

完整函数内容为
```cpp
void btCollisionWorld::contactTest(btCollisionObject * colObj, ContactResultCallback & resultCallback)
```

`contactTest`会对确定的colObj对象与`btCollisionWorld`中的所有对象进行接触检测，并调用`ContactResultCallBack`回调。
其实这个函数不算碰撞检测，只是算接触检测，如果距离为0，是会触发回调的。

#### 1.1. 继承回调的结构体

`ContactResultCallback`结构体有一个名为`addSingleResult`的纯虚函数，在继承的时候一定要实现`addSingleResult`函数。这个也是碰撞的时候执行的回调函数。是这个结构体的核心。碰撞信息会存储在`btManifoldPoint & cp`中，使用方法也比较简单，可以参考API文档的接口。其它地方的碰撞，也是用这个对象存储，处理方法是一样的。

```cpp
// 碰撞检测回调
struct MyColCallBack : btCollisionWorld::ContactResultCallback
{
    public:
        btScalar addSingleResult(
            btManifoldPoint & cp,
            const btCollisionObjectWrapper * colObj0Wrap,
            int partId0,
            int index0,
            const btCollisionObjectWrapper * colObj1Wrap,
            int partId1,
            int index1)
        {
            btVector3 posA = cp.getPositionWorldOnA();
            btVector3 posB = cp.getPositionWorldOnB();
            printf("col pos for A {%f, %f, %f}\n", posA.getX(), posA.getY(), posA.getZ());
            printf("col pos for B {%f, %f, %f}\n", posB.getX(), posB.getY(), posB.getZ());

            return btScalar(0.f);
        };
};
```

#### 1.2. 碰撞检测

```cpp
// 创建一个球体，并加入到场景中
btCollisionShape* shape = new btSphereShape(btScalar(1.f));
btTransform trans;
trans.setIdentity();
trans.setOrigin(btVector3(0, 1, 0));

btScalar mass=1.f;
btVector3 localInertia(0, 0, 0);
bool isDynamic = (mass != 0.f);
if (isDynamic)
    shape->calculateLocalInertia(mass, localInertia);

btDefaultMotionState* myMotionState = new btDefaultMotionState(trans);
btRigidBody::btRigidBodyConstructionInfo cInfo(mass, myMotionState, shape, localInertia);
btRigidBody* g_body = new btRigidBody(cInfo);
g_world->addRigidBody(g_body);

// 创建回调并碰撞检测
MyColCallBack callBack;
g_world->contactTest(g_body, callBack);

// todo delete
```

运行结果：
![result](/pics/bullet3_col_001.png)


### 2. `btCollisionWorld::performDiscreteCollisionDetection`

`performDiscreteCollisionDetection`会对场景中的所有物体进行一次碰撞检测。而`contactTest`是对确定的物体进行碰撞检测。

```cpp
g_world->performDiscreteCollisionDetection();

list<btCollisionObject*> m_collisionObjects;
int numManifolds = g_world->getDispatcher()->getNumManifolds();

for(int i=0; i<numManifolds; i++)
{
    btPersistentManifold* contactManifold = g_world->getDispatcher()->getManifoldByIndexInternal(i);
    btCollisionObject* obA = (btCollisionObject*)(contactManifold->getBody0());
    btCollisionObject* obB = (btCollisionObject*)(contactManifold->getBody1());

    int numContacts = contactManifold->getNumContacts();
    for(int j=0; j<numContacts; j++)
    {
        btManifoldPoint& pt = contactManifold->getContactPoint(j);
        if(pt.getDistance()<=0.f)
        {
            m_collisionObjects.push_back(obA);
            m_collisionObjects.push_back(obB);
            btVector3 posA = pt.getPositionWorldOnA();
            btVector3 posB = pt.getPositionWorldOnB();
            printf("%d A -> {%f, %f, %f}\n", i, posA.getX(), posA.getY(), posA.getZ()); // 碰撞点
            printf("%d B -> {%f, %f, %f}\n", i, posB.getX(), posB.getY(), posB.getZ());
        }
    }
}
```

这里需要注意一下，多个物体两两碰撞的时候，列表`m_collisionObjects`内是存在重复的可能的，往往需要去重一下。

```cpp
m_collisionObjects.sort();
m_collisionObjects.unique();
```

运行结果：
这里我多加了一个半径为1，位置为{1,1,0}的求，然后基本上两个球和地板发生了两两碰撞。
![result](/pics/bullet3_col_003.png)

### 3. `btDynamicsWorld::stepSimulation`

完整的函数内容为：
```cpp
virtual int btDynamicsWorld::stepSimulation(
    btScalar timeStep,
    int maxSubSteps = 1,
    btScalar fixedTimeStep = btScalar(1.)/btScalar(60.))
```

`stepSimulation`其实不是用来做碰撞检测的，而是用来做物理运动模拟的。既然能做运动模拟，那肯定也能够做碰撞检测了。

#### 3.1. 模拟运动

设置场景的重力加速为`btVector3(0,-10,0)`，增加一个半径为1，位置为{0,100,0}的球体，并设置其质量为1，冲量为{2,0,0}，即球体会以x轴速度为2，Y轴以-10的加速度做抛物线运动。

```cpp
// 设置重力加速度
g_world->setGravity(btVector3(0,-10,0));      

// 创建一个球体，并加入到场景中
btCollisionShape* shape = new btSphereShape(btScalar(1.f));
btTransform trans;
trans.setIdentity();
trans.setOrigin(btVector3(0, 100, 0));

btScalar mass=1.f;
btVector3 localInertia(0, 0, 0);
bool isDynamic = (mass != 0.f);
if (isDynamic)
    shape->calculateLocalInertia(mass, localInertia);

btDefaultMotionState* myMotionState = new btDefaultMotionState(trans);
btRigidBody::btRigidBodyConstructionInfo cInfo(mass, myMotionState, shape, localInertia);
btRigidBody* g_body = new btRigidBody(cInfo);
g_body->applyCentralImpulse(btVector3(2,0,0));  // 设置冲量
g_world->addRigidBody(g_body);


for (i=0;i<10;i++)
{
	g_world->stepSimulation(1.f/60.f,10);       // 模拟运动

    trans = g_body->getWorldTransform();
	printf("world pos  = %f,%f,%f\n", trans.getOrigin().getX(), 
                                      trans.getOrigin().getY(),
                                      trans.getOrigin().getZ());
	}
}
```

执行结果
![result](/pics/bullet3_col_007.png)