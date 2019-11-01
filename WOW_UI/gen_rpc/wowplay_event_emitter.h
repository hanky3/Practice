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

#ifndef WOWPLAY_EVENT_EMITTER_H
#define WOWPLAY_EVENT_EMITTER_H

/* std c header include */

/* std c++ header include */
#include <memory>
#include <string>
#include <vector>
#include <mutex>

/* lib c header include */

/* lib c++ header include */

/* my c header include */

/* my c++ header include */

/* To avoid fragmentation, UDP packet size should be smaller than MTU (1500) */
/* header of IPv4 is 20 bytes, UDP header is 8 bytes. So UDP data is 1472    */

namespace lge {
namespace wowplay {

class wowplayEventEmitter {
public:
    /* class ctors */
    wowplayEventEmitter(const wowplayEventEmitter&) = delete;
    wowplayEventEmitter& operator=(const wowplayEventEmitter&) = delete;
    wowplayEventEmitter(wowplayEventEmitter&&) = delete;
    wowplayEventEmitter& operator=(wowplayEventEmitter&&) = delete;

    /* class dtors */
    virtual ~wowplayEventEmitter() = default;

    /* public member function declaration here */
    static wowplayEventEmitter& getInstance();
    void makeReady();
    void release();

    void emitSetGroupInfoRsp(const int tid,
                             const int result);
    void emitGroupActivateRsp(const int tid,
                              const int result);
    void emitGroupDeactivateRsp(const int tid,
                                const int result);
    void emitGroupPlayRsp(const int tid,
                          const int result);
    void emitSetGroupAbsVolumeRsp(const int tid,
                                  const int result);
    void emitSetGroupRelVolumeRsp(const int tid,
                                  const int result);
    void emitSetGroupMuteRsp(const int tid,
                             const int result);
    void emitVolumeChangeInd(const int speakerIdx,
                             const int volume);
    void emitGroupPlayInd(const int play);
    void emitGroupStatusInd(const int code,
                            const int data);
    void emitAudioPlaybackInfoInd(const int bitDepth,
                                  const int sampleRate,
                                  const int audioChannel,
                                  const int playbackLatency);
    void emitwifiChannelInfoInd(const int wifiCh);

private:
    wowplayEventEmitter();
    
    static std::unique_ptr<wowplayEventEmitter> mInstance_;
    static std::once_flag mOnce_;

    class wowplayEventEmitterImpl;
    std::unique_ptr<wowplayEventEmitterImpl> mEventEmitterImpl_;
};

}  // namespace wowplay
}  // namespace lge

#endif  // WOWPLAY_EVENT_EMITTER_H
