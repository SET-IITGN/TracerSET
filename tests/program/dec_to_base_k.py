def fun():
	n=5 #int(input())
	b=2 #int(input())
	s=0
	p=0
	while n>0:
		q=int(n/b)
		r=n%b
		s=s+(r*(10**p))
		p=p+1
		n=q

	print(s)
	
fun()
