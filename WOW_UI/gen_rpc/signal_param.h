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

#ifndef SIGNAL_PARAM_H
#define SIGNAL_PARAM_H

/* std c header include */

/* std c++ header include */
#include <vector>
#include <utility>
#include <string>

/* lib c header include */

/* lib cpp header include */
#include <boost/variant.hpp>
#include <boost/serialization/vector.hpp>
#include <boost/serialization/variant.hpp>
#include <boost/serialization/utility.hpp>
#include <boost/archive/binary_oarchive.hpp>
#include <boost/archive/binary_iarchive.hpp>

/* my c header include */

/* my cpp header include */

namespace lge {
namespace comm {

class SignalParams {
public:
    using param_any_varant = boost::variant<int, double, bool, std::string, std::vector<uint8_t>>;
    using Param_t = std::pair<std::string, param_any_varant>;
    using Params_t = std::vector<Param_t>;

    void putInt(const std::string& name, const int i);
    void putDouble(const std::string& name, const double d);
    void putString(const std::string& name, const std::string& s);
    void putBool(const std::string& name, const bool b);
    void putVector(const std::string& name, const std::vector<uint8_t>& v);

    bool isInt(const param_any_varant& operand) const;
    bool isDouble(const param_any_varant& operand) const;
    bool isString(const param_any_varant& operand) const;
    bool isBool(const param_any_varant& operand) const;
    bool isVector(const param_any_varant& operand) const;

    int getInt(const param_any_varant& operand) const;
    double getDouble(const param_any_varant& operand) const;
    std::string getString(const param_any_varant& operand) const;
    bool getBool(const param_any_varant& operand) const;
    std::vector<uint8_t> getVector(const param_any_varant& operand) const;

    void clear();

    Params_t::const_iterator cbegin() const {
        return mParams_.cbegin();
    }
    Params_t::const_iterator cend() const {
        return mParams_.cend();
    }

    friend std::ostream& operator<<(std::ostream& os, const SignalParams& params);

private:
    friend class boost::serialization::access;

    Params_t mParams_;

    template <class Archive>
    void serialize(Archive& ar, const uint32_t /*verstion*/) {
        ar & mParams_;
    }
};

}  // namespace comm
}  // namespace lge

#endif  // SIGNAL_PARAM_H
