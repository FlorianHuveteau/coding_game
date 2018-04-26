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
