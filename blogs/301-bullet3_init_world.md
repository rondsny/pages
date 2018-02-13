title: "[Bullet3]创建世界(场景)及常见函数"
date: 2017-02-06 20:16:57
tags: Bullet3
---

## 创建世界(场景)及常见函数

官方文档：http://bulletphysics.org
开源代码：https://github.com/bulletphysics/bullet3/releases
API文档：http://bulletphysics.org/Bullet/BulletFull/annotated.html

### 0. 世界的继承类

- `btCollisionWorld`
    - 基类
- `btDynamicsWorld`
    - 继承于`btCollisionWorld`
    - 基础的动力学实现
- `btDiscreteDynamicsWorld`
    - 继承于`btDynamicsWorld`
    - 刚体的运动模拟

### 1. 创建世界(场景)

```cpp
// 初始化场景

// 用于配置碰撞检测堆栈大小，默认碰撞算法，接触副本池的大小
btDefaultCollisionConfiguration* collisionConfiguration = new btDefaultCollisionConfiguration();

// 用于计算重叠对象（碰撞检测，接触点计算）（接触点会被封装成 btPersistentManifold 对象）
btCollisionDispatcher* dispatcher = new btCollisionDispatcher(collisionConfiguration);

// 提供成对的aabb重叠监测（重叠对象的管理，存储，增加删除等）
btBroadphaseInterface* overlappingPairCache = new btDbvtBroadphase();

btSequentialImpulseConstraintSolver* solver = new btSequentialImpulseConstraintSolver;
btDynamicsWorld* world = new btDiscreteDynamicsWorld(dispatcher, overlappingPairCache, solver, collisionConfiguration);

```

### 2. 场景函数

- `void btDynamicsWorld::addRigidBody(btRigidBody* body)`
    - 添加一个刚体
- `void btCollisionWorld::removeCollisionObject(btCollisionObject* collisionObject)`
    - 删除对象
- `int btCollisionWorld::getNumCollisionObjects()`
    - 获取数量
- `btAlignedObjectArray<btCollisionObject*> btCollisionWorld::getCollisionObjectArray()`
    - 获取场景所有对象
- `void	btDynamicsWorld::setGravity(const btVector3& gravity)`
    - 设置重力
    - 默认值：btVector3(0,0,0)
- `void	btDynamicsWorld::performDiscreteCollisionDetection()`
    - 碰撞检测
- `int btDynamicsWorld::stepSimulation(btScalar timeStep, int maxSubSteps = 1, btScalar fixedTimeStep = btScalar(1.)/btScalar(60.))`
    - 模拟运动


### 3. 举例

1. 场景场景；
2. 添加一个刚体；
3. 释放内存退出。

```cpp
#include "btBulletDynamicsCommon.h"
#include <stdio.h>

int main(int argc, char** argv)
{
    int i;
    ///-----initialization_start-----

    ///collision configuration contains default setup for memory, collision setup. Advanced users can create their own configuration.
    btDefaultCollisionConfiguration* collisionConfiguration = new btDefaultCollisionConfiguration();

    ///use the default collision dispatcher. For parallel processing you can use a diffent dispatcher (see Extras/BulletMultiThreaded)
    btCollisionDispatcher* dispatcher = new	btCollisionDispatcher(collisionConfiguration);

    ///btDbvtBroadphase is a good general purpose broadphase. You can also try out btAxis3Sweep.
    btBroadphaseInterface* overlappingPairCache = new btDbvtBroadphase();

    ///the default constraint solver. For parallel processing you can use a different solver (see Extras/BulletMultiThreaded)
    btSequentialImpulseConstraintSolver* solver = new btSequentialImpulseConstraintSolver;

    btDiscreteDynamicsWorld* dynamicsWorld = new btDiscreteDynamicsWorld(dispatcher,overlappingPairCache,solver,collisionConfiguration);

    dynamicsWorld->setGravity(btVector3(0,-10,0));

    ///-----initialization_end-----

    //keep track of the shapes, we release memory at exit.
    //make sure to re-use collision shapes among rigid bodies whenever possible!
    btAlignedObjectArray<btCollisionShape*> collisionShapes;


    ///create a few basic rigid bodies
    btCollisionShape* groundShape = new btBoxShape(btVector3(btScalar(50.),btScalar(50.),btScalar(50.)));

    btTransform groundTransform;
    groundTransform.setIdentity();
    groundTransform.setOrigin(btVector3(0,-56,0));

    btScalar mass(0.);

    //rigidbody is dynamic if and only if mass is non zero, otherwise static
    bool isDynamic = (mass != 0.f);

    btVector3 localInertia(0,0,0);
    if (isDynamic)
        groundShape->calculateLocalInertia(mass,localInertia);

    //using motionstate is optional, it provides interpolation capabilities, and only synchronizes 'active' objects
    btDefaultMotionState* myMotionState = new btDefaultMotionState(groundTransform);
    btRigidBody::btRigidBodyConstructionInfo rbInfo(mass,myMotionState,groundShape,localInertia);
    btRigidBody* body = new btRigidBody(rbInfo);

    //add the body to the dynamics world
    dynamicsWorld->addRigidBody(body);

    //cleanup in the reverse order of creation/initialization
    delete body;
    delete myMotionState;
    delete groundShape;

    delete dynamicsWorld;
    delete solver;
    delete overlappingPairCache;
    delete dispatcher;
    delete collisionConfiguration;
}

```