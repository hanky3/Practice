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
#include "wowplay_event_emitter.h"

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
#include <memory>
#include <mutex>
#include <unordered_set>
#include <exception>

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


class wowplayEventEmitter::wowplayEventEmitterImpl {
public:
    /* class ctors */
    wowplayEventEmitterImpl(const std::string& name, const uint32_t data_size) : mThreadStop_{false} {
        mName_ = "/tmp/" + name;
        mDataBuffer_ = std::make_shared<std::vector<char> >(data_size, 0);

        mSocket_ = socket(PF_FILE, SOCK_DGRAM, 0);
        if (mSocket_ < 0) {
            std::cerr << __func__ << " ERROR : create socket" << std::endl;
            throw std::runtime_error("fail socket open");
        }

        if (access(mName_.c_str(), F_OK) == 0) {
            unlink(mName_.c_str());
        }

        struct sockaddr_un addr;
        std::memset(&addr, 0, sizeof(addr));
        addr.sun_family = AF_UNIX;
        std::strcpy(addr.sun_path, mName_.c_str());
        if (bind(mSocket_, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            std::cerr << __func__ << " ERROR : socket bind" << std::endl;
            close(mSocket_);
            mSocket_ = 0;
            throw std::runtime_error("fail socket bind");
        }

        mThread_ = std::thread(&wowplayEventEmitterImpl::mainLoopThread_, this);
        std::cerr << __func__ << " INFO : done" << std::endl;
    }

    void release() {
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
        std::cerr << __func__ << " INFO : done" << std::endl;
    }

    void emitSetGroupInfoRsp(const int tid,
                             const int result) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "SetGroupInfoRsp");
        sig_param.putInt("tid", tid);
        sig_param.putInt("result", result);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitGroupActivateRsp(const int tid,
                              const int result) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "GroupActivateRsp");
        sig_param.putInt("tid", tid);
        sig_param.putInt("result", result);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitGroupDeactivateRsp(const int tid,
                                const int result) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "GroupDeactivateRsp");
        sig_param.putInt("tid", tid);
        sig_param.putInt("result", result);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitGroupPlayRsp(const int tid,
                          const int result) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "GroupPlayRsp");
        sig_param.putInt("tid", tid);
        sig_param.putInt("result", result);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitSetGroupAbsVolumeRsp(const int tid,
                                  const int result) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "SetGroupAbsVolumeRsp");
        sig_param.putInt("tid", tid);
        sig_param.putInt("result", result);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitSetGroupRelVolumeRsp(const int tid,
                                  const int result) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "SetGroupRelVolumeRsp");
        sig_param.putInt("tid", tid);
        sig_param.putInt("result", result);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitSetGroupMuteRsp(const int tid,
                             const int result) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "SetGroupMuteRsp");
        sig_param.putInt("tid", tid);
        sig_param.putInt("result", result);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitVolumeChangeInd(const int speakerIdx,
                             const int volume) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "VolumeChangeInd");
        sig_param.putInt("speakerIdx", speakerIdx);
        sig_param.putInt("volume", volume);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitGroupPlayInd(const int play) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "GroupPlayInd");
        sig_param.putInt("play", play);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitGroupStatusInd(const int code,
                            const int data) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "GroupStatusInd");
        sig_param.putInt("code", code);
        sig_param.putInt("data", data);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitAudioPlaybackInfoInd(const int bitDepth,
                                  const int sampleRate,
                                  const int audioChannel,
                                  const int playbackLatency) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "AudioPlaybackInfoInd");
        sig_param.putInt("bitDepth", bitDepth);
        sig_param.putInt("sampleRate", sampleRate);
        sig_param.putInt("audioChannel", audioChannel);
        sig_param.putInt("playbackLatency", playbackLatency);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

    void emitwifiChannelInfoInd(const int wifiCh) {
        BEGIN_DATA_SERIALIZE_();

        sig_param.putString("sig_name", "wifiChannelInfoInd");
        sig_param.putInt("wifiCh", wifiCh);

        END_DATA_SERIALIZE_();
        sendMessage_(buffer_, buffer_.size());
    }

private:
    int32_t mSocket_;
    bool mThreadStop_;
    std::string mName_;
    std::thread mThread_;
    std::mutex mMutex_;
    std::unordered_set<int32_t> mListeners_;
    std::shared_ptr<std::vector<char> > mDataBuffer_;

    int32_t sendMessage_(std::vector<char>& msg, const int32_t length) {
        if (mSocket_ <= 0) {
            std::cerr << __func__ << " ERROR : not ready" << std::endl;
            return -1;
        }

        std::lock_guard<std::mutex> lock{mMutex_};
        for (auto it : mListeners_) {
            std::string filepath = mName_ + std::to_string(it);
            struct sockaddr_un target_addr;
            std::memset(&target_addr, 0, sizeof(target_addr));
            target_addr.sun_family = AF_UNIX;
            std::strcpy(target_addr.sun_path, filepath.c_str());

            sendto(mSocket_, msg.data(), length, 0, (struct sockaddr*)&target_addr, sizeof(target_addr));
            // TODO(Jaehoon Kim): if sendto is error, erase the lisner
        }
        return 0;
    }

    int32_t listenerManager_(std::shared_ptr<std::vector<char> > msg, const int32_t length) {
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
            std::cout << __func__ << " INFO : signal name = " << signal_name << std::endl;
        } else {
            std::cout << __func__ << " ERROR : there is no signal name" << std::endl;
            return -1;
        }

        if (!signal_name.compare("listenerAdd")) {
            int32_t id = sig_param.getInt((++pos)->second);
            std::cout << __func__ << " INFO : add listener  " << id << std::endl;
            std::lock_guard<std::mutex> lock{mMutex_};
            mListeners_.insert(id);
        }
        if (!signal_name.compare("listenerRemove")) {
            int32_t id = sig_param.getInt((++pos)->second);
            std::cout << __func__ << " INFO : remove listener  " << id << std::endl;
            std::lock_guard<std::mutex> lock{mMutex_};
            mListeners_.erase(id);
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

            // stop signal contain all zero data in first three bytes
            if (mDataBuffer_->at(0) == 0 && mDataBuffer_->at(1) == 0 && mDataBuffer_->at(2) == 0) {
                std::cerr << __func__ << " INFO : stop or invalid format" << std::endl;
                continue;
            }

            // after call handler, reply message will be in mBuffer_
            listenerManager_(mDataBuffer_, rtn);
        }
        std::cerr << __func__ << " INFO : stop" << std::endl;
    }
};

std::unique_ptr<wowplayEventEmitter> wowplayEventEmitter::mInstance_;
std::once_flag wowplayEventEmitter::mOnce_;

wowplayEventEmitter::wowplayEventEmitter() {
    mEventEmitterImpl_.reset(new wowplayEventEmitterImpl("wowplayEvent", 1280));
}

wowplayEventEmitter& wowplayEventEmitter::getInstance() {
    std::call_once(mOnce_, []() {
        mInstance_.reset(new wowplayEventEmitter);
    });
    return *(mInstance_.get());
}

void wowplayEventEmitter::makeReady() {
}

void wowplayEventEmitter::release() {
    mEventEmitterImpl_->release();
}

void wowplayEventEmitter::emitSetGroupInfoRsp(const int tid,
                                              const int result) {
    mEventEmitterImpl_->emitSetGroupInfoRsp(tid, result);
}

void wowplayEventEmitter::emitGroupActivateRsp(const int tid,
                                               const int result) {
    mEventEmitterImpl_->emitGroupActivateRsp(tid, result);
}

void wowplayEventEmitter::emitGroupDeactivateRsp(const int tid,
                                                 const int result) {
    mEventEmitterImpl_->emitGroupDeactivateRsp(tid, result);
}

void wowplayEventEmitter::emitGroupPlayRsp(const int tid,
                                           const int result) {
    mEventEmitterImpl_->emitGroupPlayRsp(tid, result);
}

void wowplayEventEmitter::emitSetGroupAbsVolumeRsp(const int tid,
                                                   const int result) {
    mEventEmitterImpl_->emitSetGroupAbsVolumeRsp(tid, result);
}

void wowplayEventEmitter::emitSetGroupRelVolumeRsp(const int tid,
                                                   const int result) {
    mEventEmitterImpl_->emitSetGroupRelVolumeRsp(tid, result);
}

void wowplayEventEmitter::emitSetGroupMuteRsp(const int tid,
                                              const int result) {
    mEventEmitterImpl_->emitSetGroupMuteRsp(tid, result);
}

void wowplayEventEmitter::emitVolumeChangeInd(const int speakerIdx,
                                              const int volume) {
    mEventEmitterImpl_->emitVolumeChangeInd(speakerIdx, volume);
}

void wowplayEventEmitter::emitGroupPlayInd(const int play) {
    mEventEmitterImpl_->emitGroupPlayInd(play);
}

void wowplayEventEmitter::emitGroupStatusInd(const int code,
                                             const int data) {
    mEventEmitterImpl_->emitGroupStatusInd(code, data);
}

void wowplayEventEmitter::emitAudioPlaybackInfoInd(const int bitDepth,
                                                   const int sampleRate,
                                                   const int audioChannel,
                                                   const int playbackLatency) {
    mEventEmitterImpl_->emitAudioPlaybackInfoInd(bitDepth, sampleRate, audioChannel, playbackLatency);
}

void wowplayEventEmitter::emitwifiChannelInfoInd(const int wifiCh) {
    mEventEmitterImpl_->emitwifiChannelInfoInd(wifiCh);
}

}  // namespace wowplay
}  // namespace lge
