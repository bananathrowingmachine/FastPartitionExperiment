#ifndef DPVERTEX
#define DPVERTEX
/*
A simple vertex class to store a dynamic programming subproblem. Uses adjacency lists.

Made by bananathrowingmachine
[date]
*/
#include <tuple>

using std::tuple;

class dpVertex
{
private:
    tuple<int, int> identifer;

    tuple<dpVertex*, dpVertex*> subproblems;

    int answer;
public:
    dpVertex(int index, int goal);

    ~dpVertex();

    void linkSubproblem(bool with, dpVertex* subproblem);

    dpVertex* getSubproblem(bool with);

    tuple<int, int> getIdentifier();

    void setAnswer(int ans);

    int getAnswer();
};
#endif