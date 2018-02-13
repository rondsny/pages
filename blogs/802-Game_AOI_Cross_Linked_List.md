title: "[game]十字链表的AOI算法实现"
date: 2016-11-29 15:30:00
tags: [AOI,算法,十字链表]
---

AOI主要有九宫格、灯塔和十字链表的算法实现。本文阐述十字链表的实现和尝试。

### 1. 基本原理

根据二维地图，将其分成x轴和y轴两个链表。如果是三维地图，则还需要维护多一个z轴的链表。将对象的坐标值按照大小相应的排列在相应的坐标轴上面。

### 2. 基本接口

对对象的操作主要有以下三个接口：

- add：对象进入地图；
- leave：对象离开地图；
- move：对象在地图内移动。

### 2. 算法实现

既然是链表，很自然地想到用线性表来实现。因为存在向前和向后找的情况，所以使用双链表实现。其实实现也是非常简单，就是两个双链表（这里以二维地图举例）。那么我们的节点需要四个指针，分布为x轴的前后指针，y轴的前后指针。

```cpp
// 双链表（对象）
class DoubleNode
{
public:
	DoubleNode(string key, int x, int y)
	{
		this->key = key;
		this->x = x;
		this->y = y;
		xPrev = xNext = NULL;
	};
	
	DoubleNode * xPrev;
	DoubleNode * xNext;
	
	DoubleNode * yPrev;
	DoubleNode * yNext;
	
	string key;  // 只是一个关键字
	int x; // 位置（x坐标）
	int y; // 位置（y坐标）

private:

};
```

下面是地图场景信息和接口。这里的实现比较粗略，是带头尾的的双链表，暂时不考虑空间占用的问题。类`Scene`有分别有一个头尾指针，初始化的时候会为其赋值，主要用`DoubleNode`类的指针来存储x轴和y轴的头尾。初始化的时候，将`_head`的next指针指向尾`_tail`；将`_tail`的prev指针指向`_head`。

```cpp
// 地图/场景
class Scene
{
public:
	Scene()
	{
		this->_head = new DoubleNode("[head]", 0, 0); // 带头尾的双链表(可优化去掉头尾)
		this->_tail = new DoubleNode("[tail]", 0, 0);
		_head->xNext = _tail;
		_head->yNext = _tail;
		_tail->xPrev = _head;
		_tail->yPrev = _head;
	};

	// 对象加入(新增)
	DoubleNode * Add(string name, int x, int y);

	// 对象离开(删除)
	void Leave(DoubleNode * node);

	// 对象移动
	void Move(DoubleNode * node, int x, int y);

	// 获取范围内的AOI (参数为查找范围)
	void PrintAOI(DoubleNode * node, int xAreaLen, int yAreaLen);

private:
	DoubleNode * _head;
	DoubleNode * _tail;
};
```

#### 2.1. add(进入地图)

将`DoubleNode`对象插入到十字链表中。x轴和y轴分别处理，处理方法基本一致。其实就是双链表的数据插入操作，需要从头开始遍历线性表，对比相应轴上的值的大小，插入到合适的位置。

```cpp
void _add(DoubleNode * node)
{
    // x轴处理
    DoubleNode * cur = _head->xNext;
    while(cur != NULL)
    {
        if((cur->x > node->x) || cur==_tail) // 插入数据
        {
            node->xNext = cur;
            node->xPrev = cur->xPrev;
            cur->xPrev->xNext = node;
            cur->xPrev = node;
            break;
        }
        cur = cur->xNext;
    }

    // y轴处理
    cur = _head->yNext;
    while(cur != NULL)
    {
        if((cur->y > node->y) || cur==_tail) // 插入数据
        {
            node->yNext = cur;
            node->yPrev = cur->yPrev;
            cur->yPrev->yNext = node;
            cur->yPrev = node;
            break;
        }
        cur = cur->yNext;
    }
}
```

假设可视范围为x轴2以内，y轴2以内，则运行：
1. 分别插入以下数据a(1,5)、f(6,6)、c(3,1)、b(2,2)、e(5,3)，然后插入d(3,3)，按照x轴和y轴打印其双链表结果；
2. 插入d(3,3)数据，求其可视AOI范围（如图，除了f(6,6)，其它对象都在d的可视范围内）。

控制台结果（前8行）：

![cll_005.png](/pics/cll_005.png)

步骤1结果图示：

![cll_001.png](/pics/cll_001.png)

步骤2结果图示：

![cll_002.png](/pics/cll_002.png)


#### 2.2. leave(离开地图)和move(移动)

其实都是双链表的基本操作，断掉其相应的指针就好了。按理，是需要


move和leave操作如图，move是将d(3,3)移动到(4,4)，然后再打印其AOI范围。

控制台结果：

![cll_006.png](/pics/cll_006.png)

移动后AOI范围图示：

![cll_003.png](/pics/cll_003.png)

#### 3. 完整代码实例

```cpp
#include "stdafx.h"
#include "stdio.h"
#include <iostream>
#include <string>

using namespace std;

// 双链表（对象）
class DoubleNode
{
public:
	DoubleNode(string key, int x, int y)
	{
		this->key = key;
		this->x = x;
		this->y = y;
		xPrev = xNext = NULL;
	};
	
	DoubleNode * xPrev;
	DoubleNode * xNext;
	
	DoubleNode * yPrev;
	DoubleNode * yNext;
	
	string key;
	int x; // 位置（x坐标）
	int y; // 位置（y坐标）

private:

};




// 地图/场景
class Scene
{
public:

	Scene()
	{
		this->_head = new DoubleNode("[head]", 0, 0); // 带头尾的双链表(可优化去掉头尾)
		this->_tail = new DoubleNode("[tail]", 0, 0);
		_head->xNext = _tail;
		_head->yNext = _tail;
		_tail->xPrev = _head;
		_tail->yPrev = _head;
	};

	// 对象加入(新增)
	DoubleNode * Add(string name, int x, int y)
	{
		
		DoubleNode * node = new DoubleNode(name, x, y);
		_add(node);
		return node;
	};

	// 对象离开(删除)
	void Leave(DoubleNode * node)
	{
		node->xPrev->xNext = node->xNext;
		node->xNext->xPrev = node->xPrev;
		node->yPrev->yNext = node->yNext;
		node->yNext->yPrev = node->yPrev;

		node->xPrev = NULL;
		node->xNext = NULL;
		node->yPrev = NULL;
		node->yNext = NULL;
	};

	// 对象移动
	void Move(DoubleNode * node, int x, int y)
	{
		Leave(node);
		node->x = x;
		node->y = y;
		_add(node);
	};

	// 获取范围内的AOI (参数为查找范围)
	void PrintAOI(DoubleNode * node, int xAreaLen, int yAreaLen)
	{
		cout << "Cur is: " << node->key  << "（" << node ->x << "," << node ->y << ")" << endl;
		cout << "Print AOI:" << endl;

		// 往后找
		DoubleNode * cur = node->xNext;
		while(cur!=_tail)
		{
			if((cur->x - node->x) > xAreaLen)
			{
				break;
			}
			else
			{
				int inteval = 0;
				inteval = node->y - cur->y;
				if(inteval >= -yAreaLen && inteval <= yAreaLen)
				{
					cout << "\t" << cur->key  << "(" << cur ->x << "," << cur ->y << ")" << endl;
				}
			}
			cur = cur->xNext;
		}

		// 往前找
		cur = node->xPrev;
		while(cur!=_head)
		{
			if((node->x - cur->x) > xAreaLen)
			{
				break;
			}
			else
			{
				int inteval = 0;
				inteval = node->y - cur->y;
				if(inteval >= -yAreaLen && inteval <= yAreaLen)
				{
					cout << "\t" << cur->key  << "(" << cur ->x << "," << cur ->y << ")" << endl;
				}
			}
			cur = cur->xPrev;
		}
	};

	// 调试代码
	void PrintLink()  // 打印链表(从头开始)
	{
		// 打印x轴链表
		DoubleNode * cur = _head->xNext;
		while (cur != _tail)
		{
			cout << (cur->key) << "(" << (cur->x) <<"," << (cur->y) << ") -> " ;
			cur = cur->xNext;
		}
		cout << "end" << endl;

		// 打印y轴链表
		cur = _head->yNext;
		while (cur != _tail)
		{
			cout << (cur->key) << "(" << (cur->x) <<"," << (cur->y) << ") -> " ;
			cur = cur->yNext;
		}
		cout << "end" << endl;
	};

private:
	DoubleNode * _head;
	DoubleNode * _tail;

	void _add(DoubleNode * node)
	{
		// x轴处理
		DoubleNode * cur = _head->xNext;
		while(cur != NULL)
		{
			if((cur->x > node->x) || cur==_tail) // 插入数据
			{
				node->xNext = cur;
				node->xPrev = cur->xPrev;
				cur->xPrev->xNext = node;
				cur->xPrev = node;
				break;
			}
			cur = cur->xNext;
		}

		// y轴处理
		cur = _head->yNext;
		while(cur != NULL)
		{
			if((cur->y > node->y) || cur==_tail) // 插入数据
			{
				node->yNext = cur;
				node->yPrev = cur->yPrev;
				cur->yPrev->yNext = node;
				cur->yPrev = node;
				break;
			}
			cur = cur->yNext;
		}
	}
};

// --------------------------------------------
void main()
{
	Scene scene = Scene();
	// 增加
	scene.Add("a", 1, 5);
	scene.Add("f", 6, 6);
	scene.Add("c", 3, 1);
	scene.Add("b", 2, 2);
	scene.Add("e", 5, 3);
	DoubleNode * node = scene.Add("d", 3, 3);

	scene.PrintLink();
	scene.PrintAOI(node, 2, 2);
	
	// 移动
	cout << endl << "[MOVE]" << endl;
	scene.Move(node, 4, 4);
	scene.PrintLink();
	scene.PrintAOI(node, 2, 2);

	// 删除
	cout << endl << "[LEAVE]" << endl;
	scene.Leave(node);
	scene.PrintLink();
}
```