CC = $(CROSS_COMPILE)gcc
CXX = $(CROSS_COMPILE)g++
CFLAGS = -std=c++11 -c -I./gen_rpc -I../external/usr/include 
LDFLAGS = -pthread -lrt -lstdc++ -lboost_iostreams -lboost_serialization -L../external/usr/lib

SRCS = $(wildcard ./gen_rpc/*.cpp)
SRCS += $(wildcard ./*.cpp)

OBJS = $(SRCS:%.cpp=%.o)
TARGET = wowctrl

$(TARGET) : $(OBJS)
	$(CXX) $(OBJS) -o $(TARGET) $(LDFLAGS) || exit $$?
	@echo "#######################################"
	@echo "Build Success!!"
	@echo "#######################################"

%.o : %.cpp $(HDRS)
	$(CXX) $(CFLAGS) $< -o $@

clean :
	rm $(OBJS) $(TARGET)
