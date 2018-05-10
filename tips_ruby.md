# Array manipulation
* To print an array
```ruby
puts my_array*""
```
* To map values in an array
```ruby
my_array.map(&:to_i)
```
* To apply multiple cast function to an array
```ruby
my_array.split.map{|c|c.to_i.chr}*""
```
* To create a array from a range
```ruby
(1..n).to_a
```
* to multiply all elements of an array
```ruby
ar.inject(:*)
```
# Input / Ouput
* gets
```ruby
c,*p=*$<
p[0].split.map{|x|$><<x.to_i.chr}
```
* to insert element e at index i in sequence s
```ruby
p s.insert i.to_i,e
```
