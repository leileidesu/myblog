---
title: "1-2-3"
date: 2022-06-29T21:32:17+08:00
tags: ["map","链表"]
---

今天开始做力扣的Hot100题单，即便是简答题也给我难哭了（笑，所以说，我真的需要这门文凭吗。

## 1 两数之和

> 给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。
>
> 你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。
>
> 你可以按任意顺序返回答案。

 我第一眼只能想到先排个序然后双指针，我是笨蛋.jpg，不过我记得这个可以O(n)的。

其实要用哈希表，比如target是6，第一个数是2，看到2就往map里面加一个键值对`(2,indexof(2))`，等到下次遇到4的时候，在map里面找有没有2，有的话输出4的下标和indexof(2)就可以。

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        map<int, int> map1;//建立一个map
        int n=nums.size();
        for(int i=0;i<n;i++)
        {
            if(map1.find(target - nums[i])!=map1.end())//是否遍历过target-num[i]
            {
                return {i,map1.find(target - nums[i])->second};
            }
            map1[nums[i]]=i;//nums[i]是第i个
        }
        return {};
    }
};
```

**来个经典的**

```cpp
map<int, int> map1;
```

定义map。

```cpp
if(map1.find(target - nums[i])!=map1.end())
```

判断map里有没有元素用的。

```cpp
map1[nums[i]]=i;
```

增加键值对的方式。



## 2 两数相加

>给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。
>
>请你将两个数相加，并以相同形式返回一个表示和的链表。
>
>你可以假设除了数字 0 之外，这两个数都不会以 0 开头。
>
>![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2021/01/02/addtwonumber1.jpg)



**注意**

**每个链表中的节点数在范围 `[1, 100]` 内**

也就是会有一百位的数字，不能用先计算再建立链表的方式了，只能模拟。

就像手写加法一样emmmm。



```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
using namespace std;
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* tmp1=l1,*tmp2=l2,*head=new ListNode(),*ans=head;
        int n=0;
        int jin=0;
        while(tmp1!=NULL || tmp2!=NULL ||jin!=0)
        {
            n=0;
            if(tmp1!=NULL)
            n+=(tmp1->val);
            if(tmp2!=NULL)
            n+=(tmp2->val);
            n+=jin;
            ans->val=n%10;
            jin=n/10;
            if(tmp1!=NULL)
            tmp1=tmp1->next;
            if(tmp2!=NULL)
            tmp2=tmp2->next;
            if(tmp1!=NULL||tmp2!=NULL||jin!=0)
            {
                ans->next=new ListNode();
            }   
            ans=ans->next;
        }
        return head;    
    }
};
```



就是从l1,l2的头部开始一个个加。

**怎么处理一个加数长一个加数短**

循环的条件是`  while(tmp1!=NULL || tmp2!=NULL ||jin!=0)`，也就是，如果两个加数都没有这一位可以加，也没有之前的进位，就没必要再算了。

在循环体里也要单独判断l1,l2，如果不是NULL才能取出val计算，否则就算0，循环体末尾的`tmp1=tmp1->next;`为了防止越界也要加一个判断条件。

**怎么处理结果的链表的位数**

一开始结果就设一个链表，有需要再动态加，有需要的意思就是`if(tmp1!=NULL||tmp2!=NULL||jin!=0)`，也就是两个加数至少有一个可以加的或者有进位。



话说回来，cpp的结构体也挺神奇的，还能有成员函数，之前记得从哪里听到过，cpp的结构体和类基本没什么区别，好像就是什么默认访问权限还是默认继承等级不同......



## 3 无重复字符的最长子串

>给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长子串** 的长度。
>
>**提示：**
>
>- `0 <= s.length <= 5 * 104`
>- `s` 由英文字母、数字、符号和空格组成

这个题做的时间不是那么长，不过错了很多次。

```cpp
#include<stdlib.h>
using namespace std;
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int n=s.length();
        int ans=0,tmp=0,begin=0;//本轮寻找的起点
        int k[130];//每个字符上次出现的位置
        memset(k,-1,sizeof(k));
        int i;
        for(i=0;i<n;i++)
        {
            if(k[s[i]]<begin)
            {
                tmp++;
            }
            else
            {
                ans=ans<tmp?tmp:ans;//记录最长的长度
                tmp-=(k[s[i]]-begin);
                begin=k[s[i]]+1;
            }
            k[s[i]]=i;
        }
        ans=ans<tmp?tmp:ans;//坑：有可能没进入过else
        return ans;
    }
};
```

如果输入的是pwwkew，前两个pw都没有问题，遍历到第三个w的时候，因为k[w]==1，代表w在下标1处出现过，代表**需要换一个起点**（不是说当前子串长度需要清0），所以更新一下ans，新的起点应该需要从**上一次w出现的地方的下一个字母**开始算，当前子串的长度tmp也要减去新旧起点的差。

