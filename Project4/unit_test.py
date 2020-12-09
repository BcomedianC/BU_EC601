def beq(x,y):
	return (x==y)
    
def test_beq():
	assert beq(1,2) == False
	assert beq(3,3) == True
