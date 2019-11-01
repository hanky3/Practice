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

#ifndef WOWPLAY_SERVICE_PROVIDER_H
#define WOWPLAY_SERVICE_PROVIDER_H

/* std c header include */

/* std c++ header include */
#include <string>
#include <vector>
#include <memory>
#include <thread>

/* lib c header include */

/* lib c++ header include */

/* my c header include */

/* my c++ header include */

/* To avoid fragmentation, UDP packet size should be smaller than MTU (1500) */
/* header of IPv4 is 20 bytes, UDP header is 8 bytes. So UDP data is 1472    */

namespace lge {
namespace wowplay {

struct wowplayServiceProviderInterface {
    virtual ~wowplayServiceProviderInterface() = default;

    virtual  int SetControllerAddr(const std::string& addr) = 0;
    virtual  std::vector<uint8_t> GetGroupInfo() = 0;
    virtual  int SetGroupInfoReq(const int cid,
                                 const int tid,
                                 const std::vector<uint8_t>& totalGroupInfo) = 0;
    virtual  int GroupActivateReq(const int cid,
                                  const int tid,
                                  const std::vector<uint8_t>& activateInfo) = 0;
    virtual  int GroupDeactivateReq(const int cid,
                                    const int tid,
                                    const std::vector<uint8_t>& lastUpdatedTime) = 0;
    virtual  int GroupPlayReq(const int cid,
                              const int tid,
                              const int play) = 0;
    virtual  std::vector<uint8_t> GetGroupAbsVolume() = 0;
    virtual  int SetGroupAbsVolumeReq(const int cid,
                                      const int tid,
                                      const std::vector<uint8_t>& absVolume) = 0;
    virtual  int SetGroupRelVolumeReq(const int cid,
                                      const int tid,
                                      const std::vector<uint8_t>& relVolume) = 0;
    virtual  int SetGroupMuteReq(const int cid,
                                 const int tid,
                                 const int mute) = 0;
    virtual  std::vector<uint8_t> GetWirelessInfo() = 0;
};

class wowplayServiceProvider {
public:
    /* class ctors */
    wowplayServiceProvider() = delete;
    wowplayServiceProvider(const wowplayServiceProvider&) = delete;
    wowplayServiceProvider& operator=(const wowplayServiceProvider&) = delete;
    wowplayServiceProvider(wowplayServiceProvider&&) = delete;
    wowplayServiceProvider& operator=(wowplayServiceProvider&&) = delete;
    explicit wowplayServiceProvider(std::shared_ptr<wowplayServiceProviderInterface> service);

    /* class dtors */
    virtual ~wowplayServiceProvider();

    /* public member function declaration here */
    bool startService();
    bool stopService();

private:
    /* private member variable declaration here */
    class wowplayServiceProviderImpl;
    std::unique_ptr<wowplayServiceProviderImpl> mServiceProviderImpl_;
};

}  // namespace wowplay
}  // namespace lge

#endif  // WOWPLAY_SERVICE_PROVIDER_H
