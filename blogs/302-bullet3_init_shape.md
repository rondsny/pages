title: "[Bullet3]常见物体和初始化"
date: 2017-02-07 20:16:57
tags: Bullet3
---

官方文档：http://bulletphysics.org
开源代码：https://github.com/bulletphysics/bullet3/releases
API文档：http://bulletphysics.org/Bullet/BulletFull/annotated.html

### 1. 初始化物体

1. 物体的形状由`btCollisionShape`对象维护；
3. 物体的位置，旋转状态由`btTransform`对象维护；
3. 最终需要将物体封装成`btRigidBody`或`btSoftBody`或其它对象；
4. 然后将步骤3的对象加入到场景中。

例如

```cpp
btCollisionShape* shape = new btBoxShape(btVector3(btScalar(1000.),btScalar(10.),btScalar(1000.)));
btTransform trans;                       // 位置、旋转维护对象
trans.setIdentity();
trans.setOrigin(btVector3(0, -10, 0));   // 设置位置

btScalar mass=0.f;
btVector3 localInertia(0, 0, 0);
bool isDynamic = (mass != 0.f);
if (isDynamic)
    shape->calculateLocalInertia(mass, localInertia);  // 设置惯性

btDefaultMotionState* myMotionState = new btDefaultMotionState(trans);
btRigidBody::btRigidBodyConstructionInfo cInfo(mass, myMotionState, shape, localInertia);
btRigidBody* body = new btRigidBody(cInfo);            // 封装成刚体
g_world->addRigidBody(body);                           // 将物体添加到场景
```

### 2. 常见物体对象

- btCollisionObject 基类
- btRigidBody 刚体
- btSoftBody 流体

#### 2.1. 物体对象常用函数

- `btCollisionShape* btCollisionObject::getCollisionShape()`
    - btCollisionObject对象中获取形状维护对象
- `void btCollisionObject::setFriction(btScalar frict)`
    - 设置摩擦力
    - 默认值：0
- `void btCollisionObject::setRestitution(btScalar rest)`
    - 设置碰撞反弹系数
    - 默认值：0
- `void btRigidBody::applyImpulse(const btVector3 & impulse, const btVector3 & rel_pos)`
    - 设置冲量/动量（通过这个设置初始速度）
- `void btRigidBody::applyCentralImpulse(const btVector3 & impulse)`
    - 设置冲量/动量（通过这个设置初始速度）
    - 默认值：0

### 3. 初始化常见物体形状

http://bulletphysics.org/Bullet/BulletFull/classbtCollisionShape.html
常见的物体有长方体、球体、胶囊体、三角网格集合。

- btCollisionShap
    - 基类
- btBoxShape
    - 长方体
    - BOX_SHAPE_PROXYTYPE
- btSphereShape
    - 球体
    - SPHERE_SHAPE_PROXYTYPE
- btCapsuleShape
    - 胶囊体
    - CAPSULE_SHAPE_PROXYTYPE
- btBvhTriangleMeshShap
    - 三角网格
    - TRIANGLE_MESH_SHAPE_PROXYTYPE
- btMultiSphereShape
    - 凸球体集合
    - MULTI_SPHERE_SHAPE_PROXYTYPE
- 

#### 3.1. 物体对象常用函数

- `int btCollisionShape::getShapeType() const`
    - 获取物品类型，类型参考以下枚举
    - `#include "BulletCollision/BroadphaseCollision/btBroadphaseProxy.h" //for the shape types`

#### 3.2. 三角网格`btBvhTriangleMeshShape`

- 构造函数`btBvhTriangleMeshShape::btBvhTriangleMeshShape(btStridingMeshInterface* meshInterface,bool useQuantizedAabbCompression)`
- 构造函数`btBvhTriangleMeshShape::btBvhTriangleMeshShape(btStridingMeshInterface* meshInterface,bool useQuantizedAabbCompression, bool buildBvh = true)`
- `btTriangleIndexVertexArray`类集成于 `btStridingMeshInterface`接口。
- `btIndexedMesh` 三角网格顶点列表和索引列表维护类


##### 3.2.1. 三角网格数据假设格式如下

- 顶点表 Vertex Buff
- 三角形表 Index Buff

```cpp
#define Landscape03.txCount 1980      // 顶点数量
#define Landscape03.dxCount 11310     // 三角形数量
#include "LinearMath/btScalar.h"

btScalar Landscape03.tx[] = {         // 顶点坐标列表(三维)
-3.0.0f,3.99193.,113.3.1f,
-3.0.0f,3.18397f,117.188f,
-3.6.094f,1.63.63.,113.3.1f,
...};

unsigned short Landscape03.dx[] = {   // 三角形列表
0,1,3.
3,3.1,
3.3,4,
5,4,3,
4,5,6,
...};

```

##### 3.2.3. `btStridingMeshInterface`接口

通用高性能三角网格访问接口。

```cpp
btStridingMeshInterface* meshInterface = new btTriangleIndexVertexArray();
btIndexedMesh part;

part.m_vertexBase = (const unsigned char*)LandscapeVtx[i];
part.m_vertexStride = sizeof(btScalar) * 3;
part.m_numVertices = LandscapeVtxCount[i];
part.m_triangleIndexBase = (const unsigned char*)LandscapeIdx[i];
part.m_triangleIndexStride = sizeof( short) * 3;
part.m_numTriangles = LandscapeIdxCount[i]/3;
part.m_indexType = PHY_SHORT;

meshInterface->addIndexedMesh(part,PHY_SHORT);

bool useQuantizedAabbCompression = true;
btBvhTriangleMeshShape* trimeshShape = new btBvhTriangleMeshShape(meshInterface,useQuantizedAabbCompression);
```
#### 3.3. 长方体`btBoxShape`

- 构造函数`btBoxShape::btBoxShape(const btVector3 & boxHalfExtents)`
- 长宽高，封装成`btVector3`对象

#### 3.4. 球`btSphereShape`

- 构造函数`btSphereShape::btSphereShape(btScalar radius)`
- radius xyz轴的半径，可以设置为椭圆球

#### 3.5. 胶囊体`btCapsuleShape`

- 构造函数`btCapsuleShape::btCapsuleShape()`
- 构造函数`btCapsuleShape::btCapsuleShape(btScalar radius, btScalar height)`
- radius 胶囊体半径，可以设置为椭圆球
- height 胶囊体长度，height为圆心之间的距离
- 胶囊体的aabb的边的长度为 {radius*2, radius*2, radius*2+height}

#### 3.6. 凸球体集合`btMultiSphereShape`

- 构造函数`btMultiSphereShape (const btVector3* positions,const btScalar* radi,int numSpheres)`
- positions 球心位置集合（第一个数组地址）
- radi 球半径集合（第一个数组地址）
- numSpheres 球体数量

举例和效果

```cpp
btVector3 vectors[4];
vectors[0] = btVector3(10,10,10);
vectors[1] = btVector3(20,20,20);
vectors[2] = btVector3(30,20,20);
vectors[3] = btVector3(30,10,40);

btScalar radi[4];
radi[0] = 5.f;
radi[1] = 5.f;
radi[2] = 5.f;
radi[3] = 10.f;

btCollisionShape* shape = new btMultiSphereShape(vectors, radi, 4);
```

![example](/pics/bullet3_col_004.png)


### 4. 射线`Raycast`

- `btCollisionWorld::rayTest(const btVector3 &from, const btVector3 &to, RayResultCallback &callback)`
    - 射线检测
- `btCollisionWorld::ClosestRayResultCallback`
    - 射线回调
- 回调的`m_flags`
    - 用于设置对物体的正反面是否生效
- `btVector3 btVector3::lerp(btVector3& v, btScalar& t)`
    - 从当前坐标往v坐标方向距离t处的坐标

```cpp
// 获取第一个击中坐标
btVector3 from(0,0,0);
btVector3 to(10,10,10);
btCollisionWorld::ClosestRayResultCallback callback(from, to);
callback.m_flags = 0;               // （位运算） 击中面 标识符

world->rayTest(from, to, callback); // 射线击中检测
if(callback.hasHit())               // 但射线击中物体
{
    // 获取击中位置坐标
    btVector3 p = from.lerp(to, callback.m_closestHitFraction);
}
```

```cpp
// 获取所有击中目标
btVector3 from(0,0,0);
btVector3 to(10,10,10);
btCollisionWorld::AllHitsRayResultCallback allCallback(from, to);
allCallback.m_flags = 0;          // （位运算） 击中面 标识符

world->rayTest(from, to, allCallback);
for(int i=0; i<allCallback.m_hitFractions.size(); i++)
{
    btVector3 p = from.lerp(to, allCallback.m_hitFractions[i]);
}

```

![example](/pics/bullet3_col_005.png)