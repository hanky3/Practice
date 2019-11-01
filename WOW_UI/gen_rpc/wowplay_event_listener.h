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

#ifndef WOWPLAY_EVENT_LISTENER_H
#define WOWPLAY_EVENT_LISTENER_H

/* std c header include */

/* std c++ header include */
#include <string>
#include <vector>
#include <memory>

/* lib c header include */

/* lib c++ header include */

/* my c header include */

/* my c++ header include */

/* To avoid fragmentation, UDP packet size should be smaller than MTU (1500) */
/* header of IPv4 is 20 bytes, UDP header is 8 bytes. So UDP data is 1472    */

namespace lge {
namespace wowplay {

struct wowplayEventListenerInterface {
    virtual ~wowplayEventListenerInterface() = default;

    virtual  void onSetGroupInfoRsp(const int tid,
                                    const int result) = 0;
    virtual  void onGroupActivateRsp(const int tid,
                                     const int result) = 0;
    virtual  void onGroupDeactivateRsp(const int tid,
                                       const int result) = 0;
    virtual  void onGroupPlayRsp(const int tid,
                                 const int result) = 0;
    virtual  void onSetGroupAbsVolumeRsp(const int tid,
                                         const int result) = 0;
    virtual  void onSetGroupRelVolumeRsp(const int tid,
                                         const int result) = 0;
    virtual  void onSetGroupMuteRsp(const int tid,
                                    const int result) = 0;
    virtual  void onVolumeChangeInd(const int speakerIdx,
                                    const int volume) = 0;
    virtual  void onGroupPlayInd(const int play) = 0;
    virtual  void onGroupStatusInd(const int code,
                                   const int data) = 0;
    virtual  void onAudioPlaybackInfoInd(const int bitDepth,
                                         const int sampleRate,
                                         const int audioChannel,
                                         const int playbackLatency) = 0;
    virtual  void onwifiChannelInfoInd(const int wifiCh) = 0;
};

class wowplayEventListener {
public:
    /* class ctors */
    wowplayEventListener() = delete;
    wowplayEventListener(const wowplayEventListener&) = delete;
    wowplayEventListener& operator=(const wowplayEventListener&) = delete;
    wowplayEventListener(wowplayEventListener&&) = delete;
    wowplayEventListener& operator=(wowplayEventListener&&) = delete;
    explicit wowplayEventListener(const int32_t id, std::shared_ptr<wowplayEventListenerInterface> listener);

    /* class dtors */
    virtual ~wowplayEventListener();

    /* public member function declaration here */
    void registerEventListener(std::shared_ptr<wowplayEventListenerInterface> listener);
    void unregisterEventListener(std::shared_ptr<wowplayEventListenerInterface> listener);

    bool startListenning();
    bool stopListenning();

private:
    /* private member variable declaration here */
    class wowplayEventListenerImpl;
    std::unique_ptr<wowplayEventListenerImpl> mListenerImpl_;
};

}  // namespace wowplay
}  // namespace lge

#endif  // WOWPLAY_EVENT_LISTENER_H
