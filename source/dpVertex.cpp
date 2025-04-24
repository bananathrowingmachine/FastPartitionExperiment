/*
A simple dpVertex class to store a dpVertex of a subproblem. Uses adjacency lists.

Made by bananathrowingmachine
[date]
*/
#include <tuple>
#include "dpVertex.h"

using std::tuple;
using std::get;

dpVertex::dpVertex(int index, int goal) {
    identifer = tuple<int, int>(index, goal);
    subproblems = tuple<dpVertex*, dpVertex*>(nullptr, nullptr);
    answer = -1;
}

dpVertex::~dpVertex() {}

void dpVertex::linkSubproblem(bool with, dpVertex* subproblem) {
    if (with)
        get<0>(subproblems) = subproblem;
    else
        get<1>(subproblems) = subproblem;
}

dpVertex* dpVertex::getSubproblem(bool with) {
    if (with)
        return get<0>(subproblems);
    return get<1>(subproblems);
}

tuple<int, int> dpVertex::getIdentifier() {
    return identifer;
}

void dpVertex::setAnswer(int ans) {
    answer = ans;
}

int dpVertex::getAnswer() {
    return answer;
}

