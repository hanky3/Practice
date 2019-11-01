/*
 * Copyright (C) 2019 LG Electronics Inc. All Rights Reserved.
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
 * Author: Changyong Park
 */

/* main purpose header file: declaration header file */
#include "wowplay_service_user.h"

/* std c header include */
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/un.h>

/* std c++ header include */
#include <cstring>
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <thread>
#include <mutex>

/* lib c header include */

/* lib c++ header include */
#include <boost/iostreams/stream.hpp>
#include <boost/iostreams/device/array.hpp>
#include <boost/iostreams/device/back_inserter.hpp>

/* my c header include */

/* my c++ header include */
#include "signal_param.h"

namespace lge {
namespace wowplay {

/* static variable or static const variable default assignment here */
#define  BEGIN_DATA_SERIALIZE_()  	using stream_buffer_t = std::vector<char>; \
                                	using boost_stream_device = boost::iostreams::back_insert_device<stream_buffer_t>; \
                                	using out_stream_t = boost::iostreams::stream<boost_stream_device>; \
                                	lge::comm::SignalParams sig_param;

#define  END_DATA_SERIALIZE_()    	stream_buffer_t buffer_; \
                                	out_stream_t out_s_(buffer_); \
                                	boost::archive::binary_oarchive out_ar_(out_s_); \
                                	out_ar_ << sig_param; \
                                	out_s_.flush();

#define  DO_DATA_DESEREALIZE_(l)   	using boost_array_device = boost::iostreams::basic_array_source<char>; \
                                    using in_stream_t = boost::iostreams::stream_buffer<boost_array_device>; \
                                    lge::comm::SignalParams sig_param; \
                                    bool error = false; \
                                    try { \
                                    in_stream_t in_s_(&mDataBuffer_->front(), (l)); \
                                    boost::archive::binary_iarchive in_ar_(in_s_); \
                                    in_ar_ >> sig_param; \
                                    } catch (boost::archive::archive_exception &ex) { \
                                    std::cout << __func__ << " ERROR : serialize exception " << ex.what() << std::endl; \
                                    error = true; \
                                    } \
                                    std::string signal_name; \
                                    auto pos = sig_param.cbegin(); \
                                    if (sig_param.isString(pos->second)) { \
                                    signal_name = sig_param.getString(pos->second); \
                                    std::cout << __func__ << " INFO : reply name = " << signal_name << std::endl; \
                                    } else { \
                                    std::cout << __func__ << " ERROR : there is no signal name" << std::endl; \
                                    error = true; \
                                    }


class wowplayServiceUser::wowplayServiceUserImpl {
public:
    /* class ctors */
    explicit wowplayServiceUserImpl(const std::string& name, const uint32_t data_size) : \
                                    mSocket_{0}, mId_{0}, mMutex_{} {
        mName_ = "/tmp/" + name;
        mDataBuffer_ = std::make_shared<std::vector<char> >(data_size, 0);
    }

    /* class dtors */
    ~wowplayServiceUserImpl() {
        if (mSocket_ > 0) {
            close(mSocket_);
        }
    }

    /* public function definition here */
    bool initialize(const int32_t id) {
        if (mId_ > 0) {
            std::cerr << __func__ << " ERROR : already initialized" << std::endl;
            return false;
        }

        mId_ = id;
        std::string filepath = mName_ + std::to_string(mId_);
        mSocket_ = socket(PF_FILE, SOCK_DGRAM, 0);
        if (mSocket_ < 0) {
            std::cerr << __func__ << " ERROR : create socket fail" << std::endl;
            return false;
        }

        if (access(filepath.c_str(), F_OK) == 0) {
            unlink(filepath.c_str());
        }

        struct sockaddr_un addr;
        std::memset(&addr, 0, sizeof(addr));
        addr.sun_family = AF_UNIX;
        std::strcpy(addr.sun_path, filepath.c_str());
        if (bind(mSocket_, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            std::cerr << __func__ << " ERROR : socket bind fail" << std::endl;
            close(mSocket_);
            mSocket_ = 0;
            return false;
        }
    
        std::cerr << __func__ << " INFO : done" << std::endl;
        return true;
    }
    
    bool uninitialize() {
        if (mSocket_ > 0) {
            close(mSocket_);
        }
        mSocket_ = 0;
        std::cerr << __func__ << " INFO : done" << std::endl;
        return true;
    }


    /* api list */
    // A api consist of 5 steps
    // 1. std::lock_guard<std::mutex> lock{mMutex_};
    // 2. serialization
    // 3. sendMessage_()
    // 4. responseManager_() if sendMessage_() returns positive value
    // 5. return parameter : Int, Bool, Double, String, Vector<uint8_t>
    int SetControllerAddr(const std::string& addr) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "SetControllerAddr");
            sig_param.putString("addr", addr);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    std::vector<uint8_t> GetGroupInfo() {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "GetGroupInfo");
            ;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        std::vector<uint8_t> value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getVector((++pos)->second);;
        }

        return value;
    }

    int SetGroupInfoReq(const int cid,
                        const int tid,
                        const std::vector<uint8_t>& totalGroupInfo) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "SetGroupInfoReq");
            sig_param.putInt("cid", cid);
            sig_param.putInt("tid", tid);
            sig_param.putVector("totalGroupInfo", totalGroupInfo);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    int GroupActivateReq(const int cid,
                         const int tid,
                         const std::vector<uint8_t>& activateInfo) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "GroupActivateReq");
            sig_param.putInt("cid", cid);
            sig_param.putInt("tid", tid);
            sig_param.putVector("activateInfo", activateInfo);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    int GroupDeactivateReq(const int cid,
                           const int tid,
                           const std::vector<uint8_t>& lastUpdatedTime) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "GroupDeactivateReq");
            sig_param.putInt("cid", cid);
            sig_param.putInt("tid", tid);
            sig_param.putVector("lastUpdatedTime", lastUpdatedTime);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    int GroupPlayReq(const int cid,
                     const int tid,
                     const int play) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "GroupPlayReq");
            sig_param.putInt("cid", cid);
            sig_param.putInt("tid", tid);
            sig_param.putInt("play", play);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    std::vector<uint8_t> GetGroupAbsVolume() {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "GetGroupAbsVolume");
            ;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        std::vector<uint8_t> value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getVector((++pos)->second);;
        }

        return value;
    }

    int SetGroupAbsVolumeReq(const int cid,
                             const int tid,
                             const std::vector<uint8_t>& absVolume) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "SetGroupAbsVolumeReq");
            sig_param.putInt("cid", cid);
            sig_param.putInt("tid", tid);
            sig_param.putVector("absVolume", absVolume);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    int SetGroupRelVolumeReq(const int cid,
                             const int tid,
                             const std::vector<uint8_t>& relVolume) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "SetGroupRelVolumeReq");
            sig_param.putInt("cid", cid);
            sig_param.putInt("tid", tid);
            sig_param.putVector("relVolume", relVolume);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    int SetGroupMuteReq(const int cid,
                        const int tid,
                        const int mute) {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "SetGroupMuteReq");
            sig_param.putInt("cid", cid);
            sig_param.putInt("tid", tid);
            sig_param.putInt("mute", mute);;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        int value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getInt((++pos)->second);;
        }

        return value;
    }

    std::vector<uint8_t> GetWirelessInfo() {
        std::lock_guard<std::mutex> lock{mMutex_};
        int32_t rtn = 0;
        if (mSocket_ > 0) {
            BEGIN_DATA_SERIALIZE_();
            sig_param.putString("sig_name", "GetWirelessInfo");
            ;
            END_DATA_SERIALIZE_();
            rtn = sendMessage_(buffer_, buffer_.size(), true);
        }
        std::vector<uint8_t> value{};
        if (rtn <= 0) {
            std::cerr << __func__ << " WARN : There is no reply data" << std::endl;
            return value;
        }

        DO_DATA_DESEREALIZE_(rtn);

        if (error) {
            return value;
        }

        if (!signal_name.compare("_return")) {
            return sig_param.getVector((++pos)->second);;
        }

        return value;
    }

private:
    /* private member variable declaration here */
    int32_t mSocket_;
    int32_t mId_;
    std::string mName_;
    std::mutex mMutex_;
    std::shared_ptr<std::vector<char> > mDataBuffer_;

    /* private member function declaration here */
    int32_t sendMessage_(std::vector<char>& msg, const int32_t length, const bool wait_reply) {
        if (mSocket_ <= 0) {
            std::cerr << __func__ << " ERROR : not ready" << std::endl;
            return -1;
        }

        struct sockaddr_un target_addr;
        std::memset(&target_addr, 0, sizeof(target_addr));
        target_addr.sun_family = AF_UNIX;
        std::strcpy(target_addr.sun_path, mName_.c_str());

        // send a message
        auto rtn = sendto(mSocket_, msg.data(), length, 0, (struct sockaddr*)&target_addr, sizeof(target_addr));
        if (rtn <= 0) {
            std::cerr << __func__ << " ERROR : sendto fail" << std::endl;
            return -1;
        }

        if (!wait_reply) {
            return 0;
        }

        struct sockaddr_un client_addr;
        uint32_t addr_size = sizeof(client_addr);
        rtn = recvfrom(mSocket_, mDataBuffer_->data(), mDataBuffer_->size(), 0, \
                        (struct sockaddr*)&client_addr, &addr_size);
        if (rtn <= 0) {
            std::cerr << __func__ << " ERROR : recvfrom fail" << std::endl;
            return -1;
        }

        // caller must care the reply with responseManager_(mDataBuffer_, rlen);
        return rtn;
    }
};

wowplayServiceUser::wowplayServiceUser() {
    mServiceUserImpl_ = std::make_shared<wowplayServiceUserImpl>("wowplayService", 1280);
}

bool wowplayServiceUser::initialize(const int32_t id) {
    return mServiceUserImpl_->initialize(id);
}

void wowplayServiceUser::uninitialize() {
    mServiceUserImpl_->uninitialize();
}

int wowplayServiceUser::SetControllerAddr(const std::string& addr) {
    return mServiceUserImpl_->SetControllerAddr(addr);
}

std::vector<uint8_t> wowplayServiceUser::GetGroupInfo() {
    return mServiceUserImpl_->GetGroupInfo();
}

int wowplayServiceUser::SetGroupInfoReq(const int cid,
                                        const int tid,
                                        const std::vector<uint8_t>& totalGroupInfo) {
    return mServiceUserImpl_->SetGroupInfoReq(cid, tid, totalGroupInfo);
}

int wowplayServiceUser::GroupActivateReq(const int cid,
                                         const int tid,
                                         const std::vector<uint8_t>& activateInfo) {
    return mServiceUserImpl_->GroupActivateReq(cid, tid, activateInfo);
}

int wowplayServiceUser::GroupDeactivateReq(const int cid,
                                           const int tid,
                                           const std::vector<uint8_t>& lastUpdatedTime) {
    return mServiceUserImpl_->GroupDeactivateReq(cid, tid, lastUpdatedTime);
}

int wowplayServiceUser::GroupPlayReq(const int cid,
                                     const int tid,
                                     const int play) {
    return mServiceUserImpl_->GroupPlayReq(cid, tid, play);
}

std::vector<uint8_t> wowplayServiceUser::GetGroupAbsVolume() {
    return mServiceUserImpl_->GetGroupAbsVolume();
}

int wowplayServiceUser::SetGroupAbsVolumeReq(const int cid,
                                             const int tid,
                                             const std::vector<uint8_t>& absVolume) {
    return mServiceUserImpl_->SetGroupAbsVolumeReq(cid, tid, absVolume);
}

int wowplayServiceUser::SetGroupRelVolumeReq(const int cid,
                                             const int tid,
                                             const std::vector<uint8_t>& relVolume) {
    return mServiceUserImpl_->SetGroupRelVolumeReq(cid, tid, relVolume);
}

int wowplayServiceUser::SetGroupMuteReq(const int cid,
                                        const int tid,
                                        const int mute) {
    return mServiceUserImpl_->SetGroupMuteReq(cid, tid, mute);
}

std::vector<uint8_t> wowplayServiceUser::GetWirelessInfo() {
    return mServiceUserImpl_->GetWirelessInfo();
}

}  // namespace wowplay
}  // namespace lge
