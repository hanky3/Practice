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
#include "wowplay_service_provider.h"

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
#include <algorithm>

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


class wowplayServiceProvider::wowplayServiceProviderImpl {
public:
    /* class ctors */
    explicit wowplayServiceProviderImpl(std::shared_ptr<wowplayServiceProviderInterface> service,
                                            const std::string& name, const uint32_t data_size) : \
                                            mSocket_{0}, mThreadStop_{false}, mThread_{}, mServiceProvider_{service} {
        mName_ = "/tmp/" + name;
        mDataBuffer_ = std::make_shared<std::vector<char> >(data_size, 0);
    }

    /* public member function declaration here */
    bool startService() {
        mSocket_ = socket(PF_FILE, SOCK_DGRAM, 0);
        if (mSocket_ < 0) {
            std::cerr << __func__ << " ERROR : fail create socket" << std::endl;
            return false;
        }

        if (access(mName_.c_str(), F_OK) == 0) {
            unlink(mName_.c_str());
        }

        struct sockaddr_un addr;
        std::memset(&addr, 0, sizeof(addr));
        addr.sun_family = AF_UNIX;
        std::strcpy(addr.sun_path, mName_.c_str());
        if (bind(mSocket_, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            std::cerr << __func__ << " ERROR : fail socket bind" << std::endl;
            close(mSocket_);
            mSocket_ = 0;
            return false;
        }

        mThread_ = std::thread(&wowplayServiceProviderImpl::mainLoopThread_, this);

        std::cerr << __func__ << " INFO : done" << std::endl;
        return true;
    }

    bool stopService() {
        mThreadStop_ = true;
        std::vector<char> end_data{0, 0, 0};
        auto sock = socket(PF_FILE, SOCK_DGRAM, 0);
        if (sock > 0) {
            std::cerr << __func__ << " INFO : send stop signal" << std::endl;
            struct sockaddr_un target_addr;
            std::memset(&target_addr, 0, sizeof(target_addr));
            target_addr.sun_family = AF_UNIX;
            std::strcpy(target_addr.sun_path, mName_.c_str());
            sendto(sock, end_data.data(), end_data.size(), 0, \
                   (struct sockaddr*)&target_addr, sizeof(target_addr));
            close(sock);
        }

        std::cerr << __func__ << " INFO : join thread" << std::endl;
        if (mThread_.joinable()) {
            mThread_.join();
        }

        if (mSocket_ > 0) {
            close(mSocket_);
        }
        mSocket_ = 0;
        mServiceProvider_.reset();
        std::cerr << __func__ << " INFO : done" << std::endl;
        return true;
    }

    int32_t SetControllerAddr(const std::string& addr) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->SetControllerAddr(addr);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t GetGroupInfo() {
        BEGIN_DATA_SERIALIZE_();

        std::vector<uint8_t> rvalue = mServiceProvider_->GetGroupInfo();
        sig_param.putString("sig_name", "_return");
        sig_param.putVector("Vector", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t SetGroupInfoReq(const int cid,
                            const int tid,
                            const std::vector<uint8_t>& totalGroupInfo) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->SetGroupInfoReq(cid, tid, totalGroupInfo);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t GroupActivateReq(const int cid,
                             const int tid,
                             const std::vector<uint8_t>& activateInfo) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->GroupActivateReq(cid, tid, activateInfo);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t GroupDeactivateReq(const int cid,
                               const int tid,
                               const std::vector<uint8_t>& lastUpdatedTime) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->GroupDeactivateReq(cid, tid, lastUpdatedTime);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t GroupPlayReq(const int cid,
                         const int tid,
                         const int play) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->GroupPlayReq(cid, tid, play);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t GetGroupAbsVolume() {
        BEGIN_DATA_SERIALIZE_();

        std::vector<uint8_t> rvalue = mServiceProvider_->GetGroupAbsVolume();
        sig_param.putString("sig_name", "_return");
        sig_param.putVector("Vector", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t SetGroupAbsVolumeReq(const int cid,
                                 const int tid,
                                 const std::vector<uint8_t>& absVolume) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->SetGroupAbsVolumeReq(cid, tid, absVolume);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t SetGroupRelVolumeReq(const int cid,
                                 const int tid,
                                 const std::vector<uint8_t>& relVolume) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->SetGroupRelVolumeReq(cid, tid, relVolume);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t SetGroupMuteReq(const int cid,
                            const int tid,
                            const int mute) {
        BEGIN_DATA_SERIALIZE_();

        int rvalue = mServiceProvider_->SetGroupMuteReq(cid, tid, mute);
        sig_param.putString("sig_name", "_return");
        sig_param.putInt("Int", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

    int32_t GetWirelessInfo() {
        BEGIN_DATA_SERIALIZE_();

        std::vector<uint8_t> rvalue = mServiceProvider_->GetWirelessInfo();
        sig_param.putString("sig_name", "_return");
        sig_param.putVector("Vector", rvalue);

        END_DATA_SERIALIZE_();

        std::copy(buffer_.begin(), buffer_.end(), mDataBuffer_->begin());
        return buffer_.size();
    }

private:
    /* private member variable declaration here */
    int32_t mSocket_;
    bool mThreadStop_;
    std::string mName_;
    std::thread mThread_;
    std::shared_ptr<std::vector<char> > mDataBuffer_;
    std::shared_ptr<wowplayServiceProviderInterface> mServiceProvider_;

    /* private member function declaration here */
    int32_t requestHandler_(std::shared_ptr<std::vector<char> > msg, const int32_t length) {
        using boost_array_device = boost::iostreams::basic_array_source<char>;
        using in_stream_t = boost::iostreams::stream_buffer<boost_array_device>;
        lge::comm::SignalParams sig_param;
        try {
            in_stream_t in_s_(&msg->front(), length);
            boost::archive::binary_iarchive in_ar_(in_s_);
            in_ar_ >> sig_param;
        } catch (boost::archive::archive_exception &ex) {
            std::cout << __func__ << " ERROR : serialize exception " << ex.what() << std::endl;
            return -1;
        }

        std::string signal_name;
        auto pos = sig_param.cbegin();
        if (sig_param.isString(pos->second)) {
            signal_name = sig_param.getString(pos->second);
            std::cout << __func__ << " INFO : request name = " << signal_name << std::endl;
        } else {
            std::cout << __func__ << " ERROR : there is no name" << std::endl;
            return -1;
        }

        if (!signal_name.compare("SetControllerAddr")) {
            std::string addr = sig_param.getString((++pos)->second);
            return SetControllerAddr(addr);
        }

        if (!signal_name.compare("GetGroupInfo")) {
            
            return GetGroupInfo();
        }

        if (!signal_name.compare("SetGroupInfoReq")) {
            int cid = sig_param.getInt((++pos)->second);
            int tid = sig_param.getInt((++pos)->second);
            std::vector<uint8_t> totalGroupInfo = sig_param.getVector((++pos)->second);
            return SetGroupInfoReq(cid, tid, totalGroupInfo);
        }

        if (!signal_name.compare("GroupActivateReq")) {
            int cid = sig_param.getInt((++pos)->second);
            int tid = sig_param.getInt((++pos)->second);
            std::vector<uint8_t> activateInfo = sig_param.getVector((++pos)->second);
            return GroupActivateReq(cid, tid, activateInfo);
        }

        if (!signal_name.compare("GroupDeactivateReq")) {
            int cid = sig_param.getInt((++pos)->second);
            int tid = sig_param.getInt((++pos)->second);
            std::vector<uint8_t> lastUpdatedTime = sig_param.getVector((++pos)->second);
            return GroupDeactivateReq(cid, tid, lastUpdatedTime);
        }

        if (!signal_name.compare("GroupPlayReq")) {
            int cid = sig_param.getInt((++pos)->second);
            int tid = sig_param.getInt((++pos)->second);
            int play = sig_param.getInt((++pos)->second);
            return GroupPlayReq(cid, tid, play);
        }

        if (!signal_name.compare("GetGroupAbsVolume")) {
            
            return GetGroupAbsVolume();
        }

        if (!signal_name.compare("SetGroupAbsVolumeReq")) {
            int cid = sig_param.getInt((++pos)->second);
            int tid = sig_param.getInt((++pos)->second);
            std::vector<uint8_t> absVolume = sig_param.getVector((++pos)->second);
            return SetGroupAbsVolumeReq(cid, tid, absVolume);
        }

        if (!signal_name.compare("SetGroupRelVolumeReq")) {
            int cid = sig_param.getInt((++pos)->second);
            int tid = sig_param.getInt((++pos)->second);
            std::vector<uint8_t> relVolume = sig_param.getVector((++pos)->second);
            return SetGroupRelVolumeReq(cid, tid, relVolume);
        }

        if (!signal_name.compare("SetGroupMuteReq")) {
            int cid = sig_param.getInt((++pos)->second);
            int tid = sig_param.getInt((++pos)->second);
            int mute = sig_param.getInt((++pos)->second);
            return SetGroupMuteReq(cid, tid, mute);
        }

        if (!signal_name.compare("GetWirelessInfo")) {
            
            return GetWirelessInfo();
        }

        return 0;
    }
    
    void mainLoopThread_() {
        std::cerr << __func__ << " INFO : start " << mName_ << std::endl;
        while (!mThreadStop_) {
            struct sockaddr_un client_addr;
            uint32_t addr_size = sizeof(client_addr);
            auto rtn = recvfrom(mSocket_, mDataBuffer_->data(), mDataBuffer_->size(), 0, \
                                (struct sockaddr*)&client_addr, &addr_size);
            if (rtn <= 0) {
                std::cerr << __func__ << " ERROR : socket was disconnected or stopped !!!" << std::endl;
                break;
            }
            // TODO(Jaehoon Kim): need to check data length?

            // stop signal contain all zero data in first three bytes
            if (mDataBuffer_->at(0) == 0 && mDataBuffer_->at(1) == 0 && mDataBuffer_->at(2) == 0) {
                std::cerr << __func__ << " INFO : stop or invalid format" << std::endl;
                continue;
            }

            auto len = requestHandler_(mDataBuffer_, rtn);
            if (len > 0) {
                sendto(mSocket_, mDataBuffer_->data(), len, 0, (struct sockaddr*)&client_addr, sizeof(client_addr));
            }
        }
        std::cerr << __func__ << " INFO : end listen a message" << std::endl;
    }
};


wowplayServiceProvider::wowplayServiceProvider(std::shared_ptr<wowplayServiceProviderInterface> service) {
    mServiceProviderImpl_.reset(new wowplayServiceProviderImpl(service, "wowplayService", 1280));
}

wowplayServiceProvider::~wowplayServiceProvider() {
    mServiceProviderImpl_->stopService();
}

bool wowplayServiceProvider::startService() {
    return mServiceProviderImpl_->startService();
}

bool wowplayServiceProvider::stopService() {
    return mServiceProviderImpl_->stopService();
}

}  // namespace wowplay
}  // namespace lge
