# pyzorder

Python implementation of z-order curve (a.k.a. Morton order)

z-order curve maps multidimensional data to one dimension.

Using z-order curve, you can implement multidimensional sort key for DynamoDB, which allows only 1 sort key at once.
pyzorder helps to implement ranging indexing with z-order curved data.

(日本語ドキュメントは、英語版の後ろにあります)

## What is "z-order curve"? 

"z-order curve" maps multidimensional data to one dimension while preserving locality of the data points.
The z value is calculated by interleaving input values.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Z-curve.svg/400px-Z-curve.svg.png)
(cited from [Z\-order curve \- Wikipedia](https://en.wikipedia.org/wiki/Z-order_curve))

Typical usage is for DynamoDB, which allows only 1 sort key at once.
For example, if you want to indexing the data with both x-axis and y-axis,
you can map x and y with z-order curve, and put the z-ordered data in the DynamoDB table as Sort Key.
However, you have to care about "unnecessary region."

![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/BIGMIN.svg/400px-BIGMIN.svg.png)  
(cited again from [Z\-order curve \- Wikipedia](https://en.wikipedia.org/wiki/Z-order_curve))

If you want to access (x = 2, ..., 3, y = 2, ..., 6), the corresponding region is dotted lines square.
When accessing z-order curve sequentially, the next value of "15" should be "36".
The region "16" to "35" is "unnecessary region."
So, you need to treat with such "unnecessary region" efficiently.

**`pyzorder` implements `next_zorder_index` which returns next valid z-order value**
You can easily implement regional indexing access with z-order curved data.

`next_zorder_index` is re-implementaion of Tropf, H.; Herzog, H. (1981), ["Multidimensional Range Search in Dynamically Balanced Trees"](http://www.vision-tools.com/h-tropf/multidimensionalrangequery.pdf) in Python.
`next_zorder_index` is shown as `BIGMIN` in the paper.

## Usage

```python
from pyzorder import ZOrderIndexer

zi = ZOrderIndexer((2, 3), (2, 6))

z_2_2 = zi.zindex(2, 2)
# z_2_2 = 12

zi.next_zorder_index(z_2_2)
# return 13

zi.next_zorder_index(15)
# return 36
```

## Reference

- [trevorprater/pymorton: A lightweight and efficient Python Morton encoder with support for geo\-hashing](https://github.com/trevorprater/pymorton)
- [Z\-order curve \- Wikipedia](https://en.wikipedia.org/wiki/Z-order_curve)
- [Z\-Order Indexing for Multifaceted Queries in Amazon DynamoDB: Part 1 \| AWS Database Blog](https://aws.amazon.com/jp/blogs/database/z-order-indexing-for-multifaceted-queries-in-amazon-dynamodb-part-1/)
- [Z\-order indexing for multifaceted queries in Amazon DynamoDB: Part 2 \| AWS Database Blog](https://aws.amazon.com/jp/blogs/database/z-order-indexing-for-multifaceted-queries-in-amazon-dynamodb-part-2/)
- Tropf, H.; Herzog, H. (1981), ["Multidimensional Range Search in Dynamically Balanced Trees"](http://www.vision-tools.com/h-tropf/multidimensionalrangequery.pdf)

# pyzorder（日本語ドキュメント）

z-order curve (a.k.a. Morton order) の Python 実装

z-order curve は多次元データを 1 次元に集約します。

pyzorder を使うことで、DynamoDB のようなソートキーを 1 つだけ持てる DB について、多次元の領域インデックスを可能にします。

## "z-order curve" とは?

z-order curve は、多次元のデータを1次元で表すための手法です。
このとき、x1 < x2 なら zorder2(x1, y) < zorder2(x2, y) という関係が常に保たれるような変換になっています。
他の次元についても同様です。

z-order curve では、各ビットをインターリーブすることで、そのようなマッピングを実現しています。

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Z-curve.svg/400px-Z-curve.svg.png)  
(cited from [Z\-order curve \- Wikipedia](https://en.wikipedia.org/wiki/Z-order_curve))

利用用途として、DynamoDB のようにソート用インデックスを 1 つだけ持てるようなデータベースに対して、
複数のカラムでのインデックスを実現したい場合に使えます。
例えば、x 座標, y 座標の両方でインデックスをしたい場合などです。
z-order curve でインターリーブした値を格納しておき、その値をソートキーにすれば、2次元データに対するインデックスが可能になります。
ただし、このとき 1 つ注意すべき点があります。

![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/BIGMIN.svg/400px-BIGMIN.svg.png)  
(cited again from [Z\-order curve \- Wikipedia](https://en.wikipedia.org/wiki/Z-order_curve))

(x = 2, ..., 3, y = 2, ..., 6) の範囲をアクセスしたい場合、この図では点線で囲まれた領域が該当します。
このとき、z-order の値を順番にたどると z-order "15" の次に範囲内となる z-order は "36" となっています。
つまり、このような 2 次元領域へアクセスする場合は、単純に z-order の値をたどるのではなく、このような "飛び地" を効率よく処理する必要があります。

**`pyzorder` は、"15" の次の有効な z-order である "36" を求める `next_zorder_index` を実装しています。**
これにより、z-order curve で表現されたデータから、任意の2次元領域へのアクセスを実現できます。

なお、`next_zorder_index` を求めるアルゴリズムは Tropf, H.; Herzog, H. (1981), ["Multidimensional Range Search in Dynamically Balanced Trees"](http://www.vision-tools.com/h-tropf/multidimensionalrangequery.pdf)
で提案されたものを Python で実装することで実現しています。（論文中の `BIGMIN` という関数が該当します）

## 使い方

```python
from pyzorder import ZOrderIndexer

zi = ZOrderIndexer((2, 3), (2, 6))

z_2_2 = zi.zindex(2, 2)
# z_2_2 = 12

zi.next_zorder_index(z_2_2)
# return 13

zi.next_zorder_index(15)
# return 36
```

## 参考

- [trevorprater/pymorton: A lightweight and efficient Python Morton encoder with support for geo\-hashing](https://github.com/trevorprater/pymorton)
- Tropf, H.; Herzog, H. (1981), ["Multidimensional Range Search in Dynamically Balanced Trees"](http://www.vision-tools.com/h-tropf/multidimensionalrangequery.pdf)
- [Z\-order curve \- Wikipedia](https://en.wikipedia.org/wiki/Z-order_curve)
- [Z\-Order Indexing for Multifaceted Queries in Amazon DynamoDB: Part 1 \| AWS Database Blog](https://aws.amazon.com/jp/blogs/database/z-order-indexing-for-multifaceted-queries-in-amazon-dynamodb-part-1/)
- [Z\-order indexing for multifaceted queries in Amazon DynamoDB: Part 2 \| AWS Database Blog](https://aws.amazon.com/jp/blogs/database/z-order-indexing-for-multifaceted-queries-in-amazon-dynamodb-part-2/)
