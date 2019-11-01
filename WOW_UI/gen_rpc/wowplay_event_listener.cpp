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
#include "wowplay_event_listener.h"

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
#include <thread>
#include <mutex>
#include <memory>
#include <unordered_set>

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


class wowplayEventListener::wowplayEventListenerImpl {
public:
    /* class ctors */
    wowplayEventListenerImpl(const int32_t id, const std::string& name, const uint32_t data_size) : \
                            mSocket_{0}, mId_{id}, mThreadStop_{false}, mThread_{}, mListener_{} {
            mName_ = "/tmp/" + name;
            mDataBuffer_ = std::make_shared<std::vector<char> >(data_size, 0);
    }

    /* public function definition here */
    bool startListenning() {
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

        if (tellToEventEmitter_(false) <= 0) {
            std::cerr << __func__ << " ERROR : fail to tell a EventEmitter" << std::endl;
            close(mSocket_);
            mSocket_ = 0;
            return false;
        }

        mThread_ = std::thread(&wowplayEventListenerImpl::mainLoopThread_, this);

        std::cerr << __func__ << " INFO : ready" << std::endl;
        return true;
    }

    bool stopListenning() {
        if (mThreadStop_) {
            std::cerr << __func__ << " INFO : already stopped" << std::endl;
            return false;
        }

        mThreadStop_ = true;
        std::vector<char> end_data{0, 0, 0};
        auto sock = socket(PF_FILE, SOCK_DGRAM, 0);
        if (sock > 0) {
            std::cerr << __func__ << " INFO : send stop signal" << std::endl;
            std::string filepath = mName_ + std::to_string(mId_);
            struct sockaddr_un target_addr;
            std::memset(&target_addr, 0, sizeof(target_addr));
            target_addr.sun_family = AF_UNIX;
            std::strcpy(target_addr.sun_path, filepath.c_str());
            sendto(sock, end_data.data(), end_data.size(), 0, \
                    (struct sockaddr*)&target_addr, sizeof(target_addr));
            close(sock);
        }

        if (tellToEventEmitter_(true) <= 0) {
            std::cerr << __func__ << " ERROR : fail to tell a EventEmitter" << std::endl;
        }

        std::cerr << __func__ << " INFO : join thread" << std::endl;
        if (mThread_.joinable()) {
            mThread_.join();
        }

        if (mSocket_ > 0) {
            close(mSocket_);
        }
        mSocket_ = 0;
        mListener_.clear();
        std::cerr << __func__ << " INFO : done" << std::endl;
        return true;
    }

    void registerEventListener(std::shared_ptr<wowplayEventListenerInterface> listener) {
        mListener_.insert(listener);
    }

    void unregisterEventListener(std::shared_ptr<wowplayEventListenerInterface> listener) {
        mListener_.erase(listener);
    }

    void onSetGroupInfoRsp(const int tid,
                           const int result) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onSetGroupInfoRsp(tid, result);
            }
        }
    }

    void onGroupActivateRsp(const int tid,
                            const int result) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onGroupActivateRsp(tid, result);
            }
        }
    }

    void onGroupDeactivateRsp(const int tid,
                              const int result) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onGroupDeactivateRsp(tid, result);
            }
        }
    }

    void onGroupPlayRsp(const int tid,
                        const int result) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onGroupPlayRsp(tid, result);
            }
        }
    }

    void onSetGroupAbsVolumeRsp(const int tid,
                                const int result) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onSetGroupAbsVolumeRsp(tid, result);
            }
        }
    }

    void onSetGroupRelVolumeRsp(const int tid,
                                const int result) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onSetGroupRelVolumeRsp(tid, result);
            }
        }
    }

    void onSetGroupMuteRsp(const int tid,
                           const int result) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onSetGroupMuteRsp(tid, result);
            }
        }
    }

    void onVolumeChangeInd(const int speakerIdx,
                           const int volume) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onVolumeChangeInd(speakerIdx, volume);
            }
        }
    }

    void onGroupPlayInd(const int play) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onGroupPlayInd(play);
            }
        }
    }

    void onGroupStatusInd(const int code,
                          const int data) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onGroupStatusInd(code, data);
            }
        }
    }

    void onAudioPlaybackInfoInd(const int bitDepth,
                                const int sampleRate,
                                const int audioChannel,
                                const int playbackLatency) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onAudioPlaybackInfoInd(bitDepth, sampleRate, audioChannel, playbackLatency);
            }
        }
    }

    void onwifiChannelInfoInd(const int wifiCh) {
        for (auto listener : mListener_) {
            if (listener) {
                listener->onwifiChannelInfoInd(wifiCh);
            }
        }
    }

private:
    /* private member variable declaration here */
    int32_t mSocket_;
    int32_t mId_;
    bool mThreadStop_;
    std::string mName_;
    std::thread mThread_;
    std::shared_ptr<std::vector<char> > mDataBuffer_;
    std::unordered_set<std::shared_ptr<wowplayEventListenerInterface>> mListener_;

    /* private function definition here */
    int32_t tellToEventEmitter_(const bool stop) {
        if (mSocket_ <= 0) {
            std::cerr << __func__ << " ERROR : socket is not ready" << std::endl;
            return -1;
        }

        using stream_buffer_t = std::vector<char>;
        using boost_stream_device = boost::iostreams::back_insert_device<stream_buffer_t>;
        using out_stream_t = boost::iostreams::stream<boost_stream_device>;
        lge::comm::SignalParams sig_param;

        if (stop) {
            sig_param.putString("sig_name", "listenerRemove");
        } else {
            sig_param.putString("sig_name", "listenerAdd");
        }
        sig_param.putInt("listenerid", mId_);

        stream_buffer_t buffer_;
        out_stream_t out_s_(buffer_);
        boost::archive::binary_oarchive out_ar_(out_s_);
        out_ar_ << sig_param;
        out_s_.flush();

        struct sockaddr_un target_addr;
        std::memset(&target_addr, 0, sizeof(target_addr));
        target_addr.sun_family = AF_UNIX;
        std::strcpy(target_addr.sun_path, mName_.c_str());

        // send a message
        return sendto(mSocket_, buffer_.data(), buffer_.size(), 0, (struct sockaddr*)&target_addr, sizeof(target_addr));
    }

    int32_t eventHandler_(std::shared_ptr<std::vector<char> > msg, const int32_t length) {
        using boost_array_device = boost::iostreams::basic_array_source<char>;
        using in_stream_t = boost::iostreams::stream_buffer<boost_array_device>;
        lge::comm::SignalParams sig_param;
        try {
            in_stream_t in_s_(&msg->front(), length);
            boost::archive::binary_iarchive in_ar_(in_s_);
            in_ar_ >> sig_param;
        } catch (boost::archive::archive_exception &ex) {
            std::cout << __func__ << " ERROR : boost serial exception " << ex.what() << std::endl;
            return -1;
        }

        std::string signal_name;
        auto pos = sig_param.cbegin();
        if (sig_param.isString(pos->second)) {
            signal_name = sig_param.getString(pos->second);
            std::cout << __func__ << " INFO : signal name = " << signal_name << std::endl;
        } else {
            std::cout << __func__ << " ERROR : there is no signal name" << std::endl;
            return -1;
        }

        if (!signal_name.compare("SetGroupInfoRsp")) {
            int tid = sig_param.getInt((++pos)->second);
            int result = sig_param.getInt((++pos)->second);
            onSetGroupInfoRsp(tid, result);
            return 0;
        }

        if (!signal_name.compare("GroupActivateRsp")) {
            int tid = sig_param.getInt((++pos)->second);
            int result = sig_param.getInt((++pos)->second);
            onGroupActivateRsp(tid, result);
            return 0;
        }

        if (!signal_name.compare("GroupDeactivateRsp")) {
            int tid = sig_param.getInt((++pos)->second);
            int result = sig_param.getInt((++pos)->second);
            onGroupDeactivateRsp(tid, result);
            return 0;
        }

        if (!signal_name.compare("GroupPlayRsp")) {
            int tid = sig_param.getInt((++pos)->second);
            int result = sig_param.getInt((++pos)->second);
            onGroupPlayRsp(tid, result);
            return 0;
        }

        if (!signal_name.compare("SetGroupAbsVolumeRsp")) {
            int tid = sig_param.getInt((++pos)->second);
            int result = sig_param.getInt((++pos)->second);
            onSetGroupAbsVolumeRsp(tid, result);
            return 0;
        }

        if (!signal_name.compare("SetGroupRelVolumeRsp")) {
            int tid = sig_param.getInt((++pos)->second);
            int result = sig_param.getInt((++pos)->second);
            onSetGroupRelVolumeRsp(tid, result);
            return 0;
        }

        if (!signal_name.compare("SetGroupMuteRsp")) {
            int tid = sig_param.getInt((++pos)->second);
            int result = sig_param.getInt((++pos)->second);
            onSetGroupMuteRsp(tid, result);
            return 0;
        }

        if (!signal_name.compare("VolumeChangeInd")) {
            int speakerIdx = sig_param.getInt((++pos)->second);
            int volume = sig_param.getInt((++pos)->second);
            onVolumeChangeInd(speakerIdx, volume);
            return 0;
        }

        if (!signal_name.compare("GroupPlayInd")) {
            int play = sig_param.getInt((++pos)->second);
            onGroupPlayInd(play);
            return 0;
        }

        if (!signal_name.compare("GroupStatusInd")) {
            int code = sig_param.getInt((++pos)->second);
            int data = sig_param.getInt((++pos)->second);
            onGroupStatusInd(code, data);
            return 0;
        }

        if (!signal_name.compare("AudioPlaybackInfoInd")) {
            int bitDepth = sig_param.getInt((++pos)->second);
            int sampleRate = sig_param.getInt((++pos)->second);
            int audioChannel = sig_param.getInt((++pos)->second);
            int playbackLatency = sig_param.getInt((++pos)->second);
            onAudioPlaybackInfoInd(bitDepth, sampleRate, audioChannel, playbackLatency);
            return 0;
        }

        if (!signal_name.compare("wifiChannelInfoInd")) {
            int wifiCh = sig_param.getInt((++pos)->second);
            onwifiChannelInfoInd(wifiCh);
            return 0;
        }

        return -1;
    }

    void mainLoopThread_() {
        std::cerr << __func__ << " INFO : start listen a event on " << mName_ << std::endl;
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

            eventHandler_(mDataBuffer_, rtn);
        }
        std::cerr << __func__ << " INFO : end listen a message" << std::endl;
    }
};

wowplayEventListener::wowplayEventListener(const int32_t id, std::shared_ptr<wowplayEventListenerInterface> listener) {
    mListenerImpl_.reset(new wowplayEventListenerImpl(id, "wowplayEvent", 1280));
    registerEventListener(listener);
}

wowplayEventListener::~wowplayEventListener() {
    mListenerImpl_->stopListenning();
    mListenerImpl_.reset();
}

void wowplayEventListener::registerEventListener(std::shared_ptr<wowplayEventListenerInterface> listener) {
    mListenerImpl_->registerEventListener(listener);
}

void wowplayEventListener::unregisterEventListener(std::shared_ptr<wowplayEventListenerInterface> listener) {
    mListenerImpl_->unregisterEventListener(listener);
}

bool wowplayEventListener::startListenning() {
    return mListenerImpl_->startListenning();
}

bool wowplayEventListener::stopListenning() {
    return mListenerImpl_->stopListenning();
}

}  // namespace wowplay
}  // namespace lge
