title: "[Bullet3]封装并引用到Erlang"
date: 2017-02-28 21:56:57
tags: Bullet3
---

官方文档：http://bulletphysics.org
开源代码：https://github.com/bulletphysics/bullet3/releases
API文档：http://bulletphysics.org/Bullet/BulletFull/annotated.html

## 封装bullet碰撞检测

该碰撞检测包含场景创建、场景物体添加、射线击中检测、胶囊体碰撞检测。

### 0. 几个文件说明

1. 将所有场景管理碰撞检测封装到ColScene类中；
2. Erlang的入口为 t_bullet.erl, C++的入口为 t_bullet.cpp；
3. data_scene.erl 为场景地形存储文件；
4. t_btest.erl 为测试场景。

### 1. ColScene类

#### 1.1. ColScene.h

```cpp
#ifndef COL_SCENE
#define COL_SCENE

#include "btBulletDynamicsCommon.h"

class ColScene
{
    private:
        btDefaultCollisionConfiguration* m_colConfig;
        btCollisionDispatcher* m_dispatcher;
        btBroadphaseInterface* m_broadInterface;
        btSequentialImpulseConstraintSolver* m_solver;
        btDynamicsWorld* m_world;  // 场景信息，退出的时候需要delete

        // add collision object
        btRigidBody* createAddRigidBody(btScalar mass, const btTransform& startTransform, btCollisionShape* shape);
        void deleteColObj(btCollisionObject* obj);
        void setColPos(btVector3 p);

    public:
        btVector3* m_colPos;       // 用于记录每次碰撞位置

        ColScene();
        ~ColScene();

        // for add 增加长方体、球体、胶囊体、三角网格到场景中
        btRigidBody* addBox(btVector3 boxHalf, btVector3 bpos, btVector4 rota, btScalar mass);
        btRigidBody* addSphere(btScalar radius, btVector3 bpos, btVector4 rota, btScalar mass);
        btRigidBody* addCupsule(
                                btScalar radius,
                                btScalar height,
                                btVector3 bpos, btVector4 rota, btScalar mass);
        btRigidBody* addTriMesh(
                                int vtxCount,
                                int idxCount,
                                btScalar vtx[],
                                unsigned short idx[],
                                btVector3 bpos, btVector4 rota, btScalar mass);

        // for check 射线检查、碰撞检测
        bool rayHit(btVector3 from, btVector3 to);
        bool checkPos(btCollisionObject* obj);
        bool checkFirstCupsule();

        // for debug
        btCollisionObject* createCapsule(btVector3 posA, btVector3 posB, double radius);
};
#endif
```

#### 1.2. ColScene.cpp

```cpp
#include <list>
#include <math.h>
#include "ColScene.h"
#include "btBulletDynamicsCommon.h"

using namespace std;

// 碰撞检测回调
struct MyColCallBack : btCollisionWorld::ContactResultCallback
{
    btVector3 m_colPos;
    bool is_col = false;

    btScalar addSingleResult(
        btManifoldPoint & cp,
        const btCollisionObjectWrapper * colObj0Wrap,
        int partId0,
        int index0,
        const btCollisionObjectWrapper * colObj1Wrap,
        int partId1,
        int index1)
    {
        m_colPos = cp.getPositionWorldOnB();
        is_col = true;
        printf("col pos {%f, %f, %f}\n", m_colPos.getX(), m_colPos.getY(), m_colPos.getZ());
        return btScalar(0.f);
    };
};

// -------------------------------
// 构造函数和析构函数
// -------------------------------
ColScene::ColScene()
{
    m_colPos = new btVector3();
    m_colConfig = new btDefaultCollisionConfiguration();
    m_dispatcher = new btCollisionDispatcher(m_colConfig);
    m_broadInterface = new btDbvtBroadphase();

    m_solver = new btSequentialImpulseConstraintSolver;
    m_world = new btDiscreteDynamicsWorld(m_dispatcher, m_broadInterface, m_solver, m_colConfig);
}

//
ColScene::~ColScene()
{
    for (int i = 0; i < m_world->getNumCollisionObjects(); ++i)
    {
        btCollisionObject* obj = m_world->getCollisionObjectArray()[i];
        deleteColObj(obj);
    }
    delete m_world;
    delete m_solver;
    delete m_broadInterface;
    delete m_dispatcher;
    delete m_colConfig;
    delete m_colPos;
}

// -------------------------------
// 私有函数
// -------------------------------
void ColScene::deleteColObj(btCollisionObject* obj)
{
    btRigidBody* body = btRigidBody::upcast(obj);
    if (body && body->getMotionState())
    {
        delete body->getMotionState();
        delete body->getCollisionShape();
    }
    m_world->removeCollisionObject(obj);
    delete obj;
}

void ColScene::setColPos(btVector3 p)
{
    printf("pos = {%f, %f, %f}\n", p.getX(), p.getY(), p.getZ());
    m_colPos->setX(p.getX());
    m_colPos->setY(p.getY());
    m_colPos->setZ(p.getZ());
}

btRigidBody* ColScene::createAddRigidBody(float mass, const btTransform& startTransform, btCollisionShape* shape)
{
    bool isDynamic = (mass != 0.f);
    btVector3 localInertia(0, 0, 0);
    if (isDynamic)
        shape->calculateLocalInertia(mass, localInertia);

    btDefaultMotionState* myMotionState = new btDefaultMotionState(startTransform);
    btRigidBody::btRigidBodyConstructionInfo cInfo(mass, myMotionState, shape, localInertia);
    btRigidBody* body = new btRigidBody(cInfo);

    m_world->addRigidBody(body);
    return body;
};

// -----------------------
// 射线检测、碰撞检测
// -----------------------
bool ColScene::rayHit(btVector3 from, btVector3 to)
{
    btCollisionWorld::ClosestRayResultCallback callback(from, to);
    m_world->rayTest(from, to, callback);
    if(callback.hasHit())
    {
        btVector3 p = callback.m_hitPointWorld;
        setColPos(p);
        return true;
    }
    return false;
}

bool ColScene::checkPos(btCollisionObject* obj)
{
    MyColCallBack cb = MyColCallBack();
    m_world->contactTest(obj, cb);
    btVector3 pos = cb.m_colPos;
    setColPos(pos);
    return cb.is_col;
}

bool ColScene::checkFirstCupsule()
{
    bool is_col = false;

    m_world->performDiscreteCollisionDetection();
    // m_world->stepSimulation(1.f/60.f);

    list<btCollisionObject*> m_collisionObjects;
    int numManifolds = m_world->getDispatcher()->getNumManifolds();

    for(int i=0; i<numManifolds; i++)
    {
        btPersistentManifold* contactManifold = m_world->getDispatcher()->getManifoldByIndexInternal(i);
        btCollisionObject* obA = (btCollisionObject*)(contactManifold->getBody0());
        btCollisionObject* obB = (btCollisionObject*)(contactManifold->getBody1());

        int numContacts = contactManifold->getNumContacts();
        for(int j=0; j<numContacts; j++)
        {
            btManifoldPoint& pt = contactManifold->getContactPoint(j);
            if(pt.getDistance()<0.f)
            {
                m_collisionObjects.push_back(obA);
                m_collisionObjects.push_back(obB);
                btVector3 posA = pt.getPositionWorldOnA();
                btVector3 posB = pt.getPositionWorldOnB();
            }
        }
    }

    if(m_collisionObjects.size()>0)
    {
        m_collisionObjects.sort();
        m_collisionObjects.unique();
        for(list<btCollisionObject*>::iterator itr = m_collisionObjects.begin(); itr != m_collisionObjects.end(); ++itr) {
            btCollisionObject* colObj = *itr;

            if(colObj->getCollisionShape()->getShapeType()==CAPSULE_SHAPE_PROXYTYPE) // 如果是胶囊体刚体
            {
                btTransform trans = colObj->getWorldTransform();
                setColPos(trans.getOrigin());
                is_col = true;
                break;
            }
        }
        m_collisionObjects.clear();
    }
    return is_col;
}

// -------------------------------
// 增加长方体、球体、胶囊体、三角网格（注意，这里会添加到场景中）
// -------------------------------
btRigidBody* ColScene::addBox(btVector3 boxHalf, btVector3 bpos, btVector4 rota, btScalar mass)
{
    btTransform trans;
    trans.setIdentity();
    trans.setOrigin(bpos);
    trans.setRotation(btQuaternion(rota.getX(), rota.getY(), rota.getZ(), rota.getW()));
    btCollisionShape* shape = new btBoxShape(boxHalf);
    return createAddRigidBody(mass, trans, shape);
};

btRigidBody* ColScene::addSphere(btScalar radius, btVector3 bpos, btVector4 rota, btScalar mass)
{
    btTransform trans;
    trans.setIdentity();
    trans.setOrigin(bpos);
    trans.setRotation(btQuaternion(rota.getX(), rota.getY(), rota.getZ(), rota.getW()));
    btCollisionShape* shape = new btSphereShape(radius);
    return createAddRigidBody(mass, trans, shape);
};

btRigidBody* ColScene::addCupsule(
                                btScalar radius,
                                btScalar height,
                                btVector3 bpos, btVector4 rota, btScalar mass)
{
    btTransform trans;
    trans.setIdentity();
    trans.setOrigin(bpos);
    trans.setRotation(btQuaternion(rota.getX(), rota.getY(), rota.getZ(), rota.getW()));
    btCollisionShape* shape = new btCapsuleShape((btScalar)radius, height);
    return createAddRigidBody(mass, trans, shape);
};

btRigidBody* ColScene::addTriMesh(
                                int vtxCount,
                                int idxCount,
                                btScalar vtx[],
                                unsigned short idx[],
                                btVector3 bpos,
                                btVector4 rota,
                                btScalar mass)
{
    btTransform trans;
    trans.setIdentity();
    trans.setOrigin(bpos);
    trans.setOrigin(btVector3(0,-25,0));
    trans.setRotation(btQuaternion(rota.getX(), rota.getY(), rota.getZ(), rota.getW()));

    btTriangleIndexVertexArray* meshInterface = new btTriangleIndexVertexArray();
    btIndexedMesh part;

    part.m_vertexBase = (const unsigned char*)vtx;
    part.m_vertexStride = sizeof(btScalar) * 3;
    part.m_numVertices = vtxCount;
    part.m_triangleIndexBase = (const unsigned char*)idx;
    part.m_triangleIndexStride = sizeof(short) * 3;
    part.m_numTriangles = idxCount/3;
    part.m_indexType = PHY_SHORT;

    meshInterface->addIndexedMesh(part, PHY_SHORT);

    bool useQuantizedAabbCompression = true;
    btBvhTriangleMeshShape* shape = new btBvhTriangleMeshShape(meshInterface, useQuantizedAabbCompression);

    return createAddRigidBody(mass, trans, shape);
};

// for debug
// -------------------------
// 创建一个胶囊体（但是不添加到场景）
btCollisionObject* ColScene::createCapsule(btVector3 posA, btVector3 posB, double radius)
{
    btScalar lenX = posB.getX() - posA.getX();
    btScalar lenY = posB.getY() - posA.getY();
    btScalar lenZ = posB.getZ() - posA.getZ();
    btScalar height = sqrt(lenX*lenX + lenY*lenY + lenZ*lenZ);

    btScalar posX = (posA.getX()+posB.getX())/2.f;
    btScalar posY = (posA.getY()+posB.getY())/2.f;
    btScalar posZ = (posA.getZ()+posB.getZ())/2.f;

    printf("lenX  -> %f\n", lenX );
    printf("lenY  -> %f\n", lenY );
    printf("lenZ  -> %f\n", lenZ );
    printf("heigh -> %f\n", height);

    printf("posX  -> %f\n", posX );
    printf("posY  -> %f\n", posY );
    printf("posZ  -> %f\n", posZ );

    btVector3 bpos(posX, posY, posZ);
    btVector4 rota(lenX, lenY, lenZ, 1.f);
    btScalar mass(1.f);

    btTransform trans;
    trans.setIdentity();
    trans.setOrigin(bpos);
    trans.setRotation(btQuaternion(rota.getX(), rota.getY(), rota.getZ(), rota.getW()));
    btCollisionShape* shape = new btCapsuleShape((btScalar)radius, height);

    bool isDynamic = (mass != 0.f);
    btVector3 localInertia(0, 0, 0);
    if (isDynamic)
        shape->calculateLocalInertia(mass, localInertia);

    btDefaultMotionState* myMotionState = new btDefaultMotionState(trans);
    btRigidBody::btRigidBodyConstructionInfo cInfo(mass, myMotionState, shape, localInertia);
    btRigidBody* body = new btRigidBody(cInfo);
    return body;
}
```

### 2. 入口

#### 2.1. Erlang项目rebar配置

```erlang

{deps,[
    {bullet3, ".*", {git, "git@github.com:bulletphysics/bullet3.git", {tag, "2.85"}}, [raw]}
]}.

{port_env, [{"linux|darwin", "CFLAGS", "$CFLAGS "},
            {"win32", "CFLAGS", "/Ox /fp:fast"}]}.

{port_specs, [
    {"win32", "priv/t_bullet.dll", [
            "c_src/t_bullet.cpp",
            "deps/bullet3/src/BulletDynamics/Character/*.cpp",
            "deps/bullet3/src/BulletDynamics/ConstraintSolver/*.cpp",
            "deps/bullet3/src/BulletDynamics/Dynamics/*.cpp",
            "deps/bullet3/src/BulletDynamics/Featherstone/*.cpp",
            "deps/bullet3/src/BulletDynamics/MLCPSolvers/*.cpp",
            "deps/bullet3/src/BulletDynamics/Vehicle/*.cpp",
            "deps/bullet3/src/BulletCollision/BroadphaseCollision/*.cpp",
            "deps/bullet3/src/BulletCollision/CollisionDispatch/*.cpp",
            "deps/bullet3/src/BulletCollision/CollisionShapes/*.cpp",
            "deps/bullet3/src/BulletCollision/Gimpact/*.cpp",
            "deps/bullet3/src/BulletCollision/NarrowPhaseCollision/*.cpp",
            "deps/bullet3/src/LinearMath/*.cpp"
            ],
         [{env, [{"CXXFLAGS", "/Ox /fp:fast  -I\"deps\\bullet3\\src\" "}]}]}

]}.

```

#### 2.2. Erlang代码入口`t_bullet.erl`

```cpp
% @Author: weiyanguang
% @Email:  rondsny@gmail.com
% @Date:   2017-01-22 18:04:28
% @Last Modified by:   weiyanguang
% @Last Modified time: 2017-02-10 11:55:43
% @Desc:

-module(t_bullet).
-export([
     open_scene/0
    ,close_scene/0

    ,add_box/3
    ,add_sphere/3
    ,add_mesh/6

    ,col_check_capsule/3
    ,ray_hit/2
    ]).

-on_load(init/0).

init() ->
    Code = filename:join("./priv", atom_to_list(?MODULE)),
    erlang:load_nif(Code, 0).

%% 初始化场景
open_scene() ->
    erlang:nif_error(undef).

%% 删除场景内资源，回收内存
close_scene() ->
    erlang:nif_error(undef).

add_box(_BoxHalf, _Bpos, _Rotation) ->
    erlang:nif_error(undef).

add_sphere(_Radius, _Bpos, _Rotation) ->
    erlang:nif_error(undef).

add_cupsule(_Radius, _Height, _Bpos, _Rotation) ->
    erlang:nif_error(undef).

add_mesh(_VtxCount, _IdxCount, _VtxList, _IdxList, _Bpos, _Rotation) ->
    erlang:nif_error(undef).

%% 检查胶囊体与场景内是否发生碰撞
%% 胶囊体两端坐标，半径
%% @return {1, {x,y,z}}| {0,{A.x, A.y, A.z}}
col_check_capsule(_PosA, _PosB, _Raduis) ->
    erlang:nif_error(undef).

%% 射线击中检测
ray_hit(_From, _To) ->
    erlang:nif_error(undef).
```

#### 2.3. C++代码入口`t_bullet.cpp`

```cpp
#include <stdio.h>
#include "erl_nif.h"
#include "btBulletDynamicsCommon.h"
#include "ColScene.h"

ColScene* g_scene;

// ---------------------------
static int get_number_f(ErlNifEnv *env, ERL_NIF_TERM eterm, double *f)
{
    if (enif_get_double(env, eterm, f)) {
        return 1;
    }
    else {
        long n;
        if (enif_get_long(env, eterm, &n)){
            *f = (double)n;
            return 1;
        }
        else {
            return 0;
        }
    }
}

static int get_vector3(ErlNifEnv *env, ERL_NIF_TERM eterm, btVector3 *vector)
{
    double x,y,z;
    int arity;
    const ERL_NIF_TERM *array;
    if (enif_get_tuple(env, eterm, &arity, &array)
        && 3 == arity
        && get_number_f(env, array[0], &x)
        && get_number_f(env, array[1], &y)
        && get_number_f(env, array[2], &z)) {

        vector->setX((btScalar)x);
        vector->setY((btScalar)y);
        vector->setZ((btScalar)z);

        return 1;
    }
    else {
        return 0;
    }
}

static int get_vector4(ErlNifEnv *env, ERL_NIF_TERM eterm, btVector4 *vector)
{
    double x,y,z,w;
    int arity;
    const ERL_NIF_TERM *array;
    if (enif_get_tuple(env, eterm, &arity, &array)
        && 4 == arity
        && get_number_f(env, array[0], &x)
        && get_number_f(env, array[1], &y)
        && get_number_f(env, array[2], &z)
        && get_number_f(env, array[3], &w)) {

        vector->setX((btScalar)x);
        vector->setY((btScalar)y);
        vector->setZ((btScalar)z);
        vector->setW((btScalar)w);

        return 1;
    }
    else {
        return 0;
    }
}

// ---------------------------

static int load(ErlNifEnv* env, void** priv, ERL_NIF_TERM load_info)
{
    return 0;
}

static int upgrade(ErlNifEnv* env, void** priv_data, void** old_priv_data, ERL_NIF_TERM load_info)
{
    return 0;
}

static ERL_NIF_TERM open_scene(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    if (!g_scene)
    {
        g_scene = new ColScene();
        printf("init scene done\n");
    }
    return enif_make_atom(env, "ok");
}

static ERL_NIF_TERM close_scene(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    delete g_scene;
    return enif_make_atom(env, "ok");
}

// ---------------------------------------------------------

static ERL_NIF_TERM add_box(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    btVector3 boxHalf;
    btVector3 bpos;
    btVector4 rota;

    if(
        get_vector3(env, argv[0], &boxHalf) &&
        get_vector3(env, argv[1], &bpos) &&
        get_vector4(env, argv[2], &rota)
    ){
        g_scene->addBox(boxHalf, bpos, rota, 0.);
        return enif_make_atom(env, "ok");
    }
    return enif_make_atom(env, "undef");
}

static ERL_NIF_TERM add_sphere(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    double radius;
    btVector3 bpos;
    btVector4 rota;

    if(
        enif_get_double(env, argv[0], &radius) &&
        get_vector3(env, argv[1], &bpos) &&
        get_vector4(env, argv[2], &rota)
    ){
        g_scene->addSphere(radius, bpos, rota, 0.);
        return enif_make_atom(env, "ok");
    }
    return enif_make_atom(env, "undef");
}

static ERL_NIF_TERM add_cupsule(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    double radius;
    double height;
    btVector3 bpos;
    btVector4 rota;

    if(
        enif_get_double(env, argv[0], &radius) &&
        enif_get_double(env, argv[1], &height) &&
        get_vector3(env, argv[2], &bpos) &&
        get_vector4(env, argv[3], &rota)
    ){
        g_scene->addCupsule(radius, height, bpos, rota, 0.);
        return enif_make_atom(env, "ok");
    }
    return enif_make_atom(env, "undef");
}

static ERL_NIF_TERM add_mesh(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    int vtxCount;
    int idxCount;
    btVector3 bpos;
    btVector4 rota;

    double vt;
    int id;
    btScalar vtx[10240];
    unsigned short idx[20480];

    ERL_NIF_TERM head;
    ERL_NIF_TERM tail;

    tail = argv[2];
    int i = 0;
    while(enif_get_list_cell(env, tail, &head, &tail))
    {
        enif_get_double(env, head, &vt);
        vtx[i] = (float)vt;
        i++;
    }

    tail = argv[3];
    i = 0;
    while(enif_get_list_cell(env, tail, &head, &tail)){
        enif_get_int(env, head, &id);
        idx[i] = (unsigned short)id;
        i++;
    }

    if(
        enif_get_int(env, argv[0], &vtxCount) &&
        enif_get_int(env, argv[1], &idxCount) &&
        get_vector3(env, argv[4], &bpos) &&
        get_vector4(env, argv[5], &rota)
    ){
        g_scene->addTriMesh(vtxCount, idxCount,
                            vtx, idx,
                            bpos, rota, 0.f);
        return enif_make_atom(env, "ok");
    }
    return enif_make_atom(env, "undef");
}

// ---------------------------------------------------------

// @return {1, {x,y,z}}| {0, {A.x, A.y, A.z}}
static ERL_NIF_TERM col_check_capsule(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    btVector3 posA;
    btVector3 posB;
    if (!get_vector3(env, argv[0], &posA))
        return enif_make_badarg(env);

    else
    {
        if (!get_vector3(env, argv[1], &posB))
            return enif_make_badarg(env);

        else
        {
            double radius;
            enif_get_double(env, argv[3], &radius);
            btCollisionObject* obj = g_scene->createCapsule(posA, posB, radius);
            int shapType = g_scene->checkPos(obj);
            if(shapType>0)
            {
                ERL_NIF_TERM termPos = enif_make_tuple3(env,
                    enif_make_double(env, g_scene->m_colPos->getX()),
                    enif_make_double(env, g_scene->m_colPos->getY()),
                    enif_make_double(env, g_scene->m_colPos->getZ()));

                ERL_NIF_TERM terms = enif_make_tuple2(env,
                    enif_make_int(env, 1),
                    termPos);
                return terms;
            }

            ERL_NIF_TERM termA = enif_make_tuple3(env,
                enif_make_double(env, posA.getX()),
                enif_make_double(env, posA.getY()),
                enif_make_double(env, posA.getZ()));

            ERL_NIF_TERM terms = enif_make_tuple2(env, enif_make_int(env, 0), termA);
            return terms;
        }
    }
}


// check raycast hit
static ERL_NIF_TERM ray_hit(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    btVector3 from;
    btVector3 to;
    if (!get_vector3(env, argv[0], &from))
        return enif_make_badarg(env);

    else
    {
        if (!get_vector3(env, argv[1], &to))
            return enif_make_badarg(env);

        else
        {
            if(g_scene->rayHit(from, to))
            {
                ERL_NIF_TERM termPos = enif_make_tuple3(env,
                    enif_make_double(env, g_scene->m_colPos->getX()),
                    enif_make_double(env, g_scene->m_colPos->getY()),
                    enif_make_double(env, g_scene->m_colPos->getZ()));

                ERL_NIF_TERM terms = enif_make_tuple2(env, enif_make_int(env, 1), termPos);
                return terms;
            }

            ERL_NIF_TERM termA = enif_make_tuple3(env,
                enif_make_double(env, from.getX()),
                enif_make_double(env, from.getY()),
                enif_make_double(env, from.getZ()));

            ERL_NIF_TERM terms = enif_make_tuple2(env, enif_make_int(env, 0), termA);
            return terms;
        }
    }
}


static ErlNifFunc nif_funcs[] = {
        {"open_scene", 0, open_scene},
        {"close_scene", 0, close_scene},

        {"add_box", 3, add_box},
        {"add_sphere", 3, add_sphere},
        {"add_cupsule", 4, add_cupsule},
        {"add_mesh", 6, add_mesh},

        {"col_check_capsule", 3, col_check_capsule},
        {"ray_hit", 2, ray_hit}
};


ERL_NIF_INIT(t_bullet, nif_funcs, load, NULL, upgrade, NULL)
``` 

### 3. 地形数据的erlang处理

#### 3.1. 定义数据格式

数据record定义

```erlang
-record(data_scene, {
        id        = 0,
        type      = undef,      % box|sphere|mesh
        position  = {0,0,0},    % 位置
        rotation  = {0,0,0,1},  % 旋转
        % 以下玩为box|sphere的内容
        scale     = {0,0,0},    % 形状，当为sphere的时候取第一个数为半径
        % 以下为mesh的内容
        vtx       = [],         % 顶点坐标
        idx       = []          % 三角形坐标索引
    }).
```

一个测试数据

```erlang
-module(data_scene).
-include("data.hrl").
-compile([export_all, {no_auto_import, [{get, 1}]}]).
gets() ->
    [
    1,
    2,
    3].

get(1) -> #data_scene{
    id       = 1,
    type     = box,
    position = {1,1,1},
    rotation = {0,0,0,1},
    scale    = {1,1,1}
};

get(2) -> #data_scene{
    id       = 2,
    type     = sphere,
    position = {1,1,1},
    rotation = {0,0,0,1},
    scale    = {1,1,1}
};

get(3) -> #data_scene{
    id       = 3,
    type     = mesh,
    position = {0,-25,0},
    rotation = {0,0,0,1},
    vtx      = [
-250.0,2.99192,113.281,
-250.0,2.18397,117.188,
-246.094,1.62262,113.281,
-246.094,1.51628,117.188,
-242.188,0.847411,113.281,
...],    
    idx      = [
0,1,2,
3,2,1,
2,3,4,
...]

...

```

#### 3.2. 初始化场景

```erlang
-module(t_btest).
-include("ts_global.hrl").
-include("data.hrl").
-compile([export_all]).

init() ->
    t_bullet:open_scene(),

    Ids = data_scene:gets(),
    Cfsg = [data_scene:get(Id)||Id<-Ids],
    lists:foreach(fun add_obj/1, Cfsg),
    ok.

add_obj(#data_scene{
            type     = box,
            position = Bpos,
            rotation = Rota,
            scale    = Scal
        }) ->
    t_bullet:add_box(Scal, Bpos, Rota);

add_obj(#data_scene{
            type     = sphere,
            position = Bpos,
            rotation = Rota,
            scale    = {Radius, _, _}
        }) ->
    t_bullet:add_sphere(Radius, Bpos, Rota);
add_obj(#data_scene{
            type     = sphere,
            position = Bpos,
            rotation = Rota,
            scale    = Radius
        }) when is_number(Radius) ->
    t_bullet:add_sphere(Radius, Bpos, Rota);
add_obj(#data_scene{
            type     = mesh,
            position = Bpos,
            rotation = Rota,
            vtx      = Vts,
            idx      = Idx
        }) ->
    t_bullet:add_mesh(length(Vts)/3, length(Idx), Vts, Idx, Bpos, Rota);
add_obj(_Unk) ->
    skip.
```

#### 3.3. 测试结果

![](pics/bullet3_col_006.png)