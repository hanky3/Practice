/*
 * Copyright (C) 2015 LG Electronics Inc. All Rights Reserved.
 * Though every care has been taken to ensure the accuracy of this document,
 * LG Electronics Inc. cannot accept responsibility for any errors or
 * omissions or for any loss occurred to any person, whether legal or natural,
 * from acting, or refraining from action, as a result of the information
 * contained herein. Information in this document is subject to change at any
 * time without obligation to notify any person of such changes.
 * LG Electronics Inc. may have patents or patent pending applications,
 * trademarks copyrights or other intellectual property rights covering subject
 * matter in this document. The furnishing of this document does not give the
 * recipient or reader any license to these patents, trademarks copyrights or
 * other intellectual property rights.
 * No part of this document may be communicated, distributed, reproduced or
 * transmitted in any form or by any means, electronic or mechanical or
 * otherwise, for any purpose, without the prior written permission of
 * LG Electronics Inc.
 * The document is subject to revision without further notice.
 * All brand names and product names mentioned in this document are trademarks
 * or registered trademarks of their respective owners
 *
 * Author: Hyugjin Kwon
 */

#define NDEBUG

/* main purpose header file: declaration header file */
#include "signal_param.h"

/* std c header include */

/* std c++ header include */
#include <ios>
#include <ostream>
#include <string>
#include <vector>

/* lib c header include */

/* lib cpp header include */
#include <boost/variant.hpp>

/* my c header include */

/* my cpp header include */

namespace lge {
namespace comm {

void SignalParams::putInt(const std::string& name,
                              const int i) {
    param_any_varant to_add(i);
    mParams_.push_back(Param_t(name, to_add));
}

void SignalParams::putDouble(const std::string& name,
                                 const double d) {
    param_any_varant to_add(d);
    mParams_.push_back(Param_t(name, to_add));
}

void SignalParams::putString(const std::string& name,
                                 const std::string& s) {
    param_any_varant to_add(s);
    mParams_.push_back(Param_t(name, s));
}

void SignalParams::putBool(const std::string& name,
                               const bool b) {
    param_any_varant to_add(b);
    mParams_.push_back(Param_t(name, to_add));
}

void SignalParams::putVector(const std::string& name,
                               const std::vector<uint8_t>& v) {
    param_any_varant to_add(v);
    mParams_.push_back(Param_t(name, to_add));
}

bool SignalParams::isInt(const param_any_varant& operand) const {
    return (operand.type() == typeid(int));
}

bool SignalParams::isDouble(const param_any_varant& operand) const {
    return (operand.type() == typeid(double));
}

bool SignalParams::isString(const param_any_varant& operand) const {
    return (operand.type() == typeid(std::string));
}

bool SignalParams::isBool(const param_any_varant& operand) const {
    return (operand.type() == typeid(bool));
}

bool SignalParams::isVector(const param_any_varant& operand) const {
    return (operand.type() == typeid(std::vector<uint8_t>));
}

int SignalParams::getInt(const param_any_varant& operand) const {
    return boost::strict_get<int>(operand);
}

double SignalParams::getDouble(const param_any_varant& operand) const {
    return boost::strict_get<double>(operand);
}

std::string SignalParams::getString(const param_any_varant& operand) const {
    return boost::strict_get<std::string>(operand);
}

bool SignalParams::getBool(const param_any_varant& operand) const {
    return boost::strict_get<bool>(operand);
}

std::vector<uint8_t> SignalParams::getVector(const param_any_varant& operand) const {
    return boost::strict_get<std::vector<uint8_t>>(operand);
}

void SignalParams::clear() {
    mParams_.clear();
}

std::ostream& operator<<(std::ostream& os,
                         const SignalParams& params) {
    std::ios::fmtflags orig_fmt(os.flags());

    for (auto pos = params.cbegin(), end = params.cend(); pos != end; ++pos) {
        os << pos->first << " = ";
        if (params.isInt(pos->second)) {
            os << params.getInt(pos->second);
        } else if (params.isDouble(pos->second)) {
            os << std::fixed << params.getDouble(pos->second);
            os.flags(orig_fmt);
        } else if (params.isString(pos->second)) {
            os << params.getString(pos->second);
        } else if (params.isBool(pos->second)) {
            os << params.getBool(pos->second);
        } else {
            os << "unknown type data";
        }
        os << std::endl;
    }

    return os;
}

}  // namespace comm
}  // namespace lge
