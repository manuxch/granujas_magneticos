# \file  Makefile
# \brief Makefile
# \author Manuel Carlevaro [IFLYSIB]
# \versión 0.1 
# \date 2018.12.17
# \note Ver: http://makepp.sourceforge.net/1.19/makepp_tutorial.html


CXX = g++
BOX2D = /home/manuel/Tools/box2d/2-4-1
LIBPATH = -L$(BOX2D)/build/bin
INCLUDES = -I$(BOX2D)/include
LIBS = -lbox2d -lm
CXXFLAGS = -O0 $(INCLUDES)
LDFLAGS = -O0 -Wall $(LIBPATH) -static $(LIBS)
#CXXFLAGS = -O3 $(INCLUDES)
#LDFLAGS = -O3 -Wall $(LIBPATH) -static $(LIBS)

OBJS = selfMag.o globalSetup.o sisAux.o

selfMag: $(OBJS)
	$(CXX) -o $@ $^ $(LDFLAGS) 

%.o : %.cpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -c $< -o $@

clean:
	rm -f *.o *~ 
 
