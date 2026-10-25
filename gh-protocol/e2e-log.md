## gh-protocol E2E log — 2026-10-25T23:23:32Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T23:22:11Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 23:18 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 23:22 .
drwxr-xr-x 3 runner runner 4096 Oct 25 23:22 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 23:22 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 23:22 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.12.0 (build_id 16428233) (CL:N/A)
INFO         | Graphics backend: gfxstream
INFO         | Found systemPath /usr/local/lib/android/sdk/system-images/android-34/google_apis/x86_64/
INFO         | Saving last run QEMU version for the AVD to 2
INFO         | Changing default hw.initialOrientation to portrait

INFO         | Increasing RAM size to 4096MB
##############################################################################
##                        WARNING - ACTION REQUIRED                         ##
##  Consider using the '-metrics-collection' flag to help improve the       ##
##  emulator by sending anonymized usage data. Or use the '-no-metrics'     ##
##  flag to bypass this warning and turn off the metrics collection.        ##
##  In a future release this warning will turn into a one-time blocking     ##
##  prompt to ask for explicit user input regarding metrics collection.     ##
##                                                                          ##
##  Please see '-help-metrics-collection' for more details. You can use     ##
##  '-metrics-to-file' or '-metrics-to-console' flags to see what type of   ##
##  data is being collected by emulator as part of usage statistics.        ##
##############################################################################
INFO         | Guest GLES Driver: Auto (ext controls)
INFO         | emuglConfig_init: vulkan_mode_selected:swiftshader gles_mode_selected:swiftshader
INFO         | Checking system compatibility:
INFO         |   Checking: hasSufficientDiskSpace
INFO         |      Ok: Disk space requirements to run avd: `gh_test` are met
INFO         |   Checking: hasSufficientHwGpu
INFO         |      Ok: Hardware GPU compatibility checks are not required
INFO         |   Checking: hasSufficientSystem
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2825
INFO         | Initializing gfxstream backend
INFO         | startOpenglesRendererImpl: gpu info
INFO         | 
INFO         | Vulkan 1.4 is not supported for the guest and won't be enabled
INFO         | initIcdPaths: ICD set to 'swiftshader', using Swiftshader ICD
INFO         | Setting ICD filenames for the loader = /usr/local/lib/android/sdk/emulator/lib64/vulkan/vk_swiftshader_icd.json
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so.1]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so]
INFO         | Added library: /usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so
INFO         | Selecting Vulkan device: SwiftShader Device (Subzero), Version: 1.3.0
INFO         | Using Vulkan externalMemoryMode: OpaqueFd for VkEmulation
INFO         | Format VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 does not support YCbCr sampler conversion
INFO         | SharedLibrary::open for [libX11]
WARNING      | Could not open libX11.so, try libX11.so.6
INFO         | SharedLibrary::open for [libX11.so.6]
INFO         | SharedLibrary::open for [libX11-xcb]
WARNING      | Could not open libX11-xcb.so, try libX11-xcb.so.1
INFO         | SharedLibrary::open for [libX11-xcb.so.1]
INFO         | Initializing VkEmulation features:
INFO         |     glInteropSupported: false
INFO         |     useDeferredCommands: true
INFO         |     createResourceWithRequirements: true
INFO         |     useVulkanComposition: false
INFO         |     useVulkanNativeSwapchain: false
INFO         |     enable guestRenderDoc: false
INFO         |     ASTC LDR emulation mode: Gpu
INFO         |     enable ETC2 emulation: true
INFO         |     enable Ycbcr emulation: false
INFO         |     guestVulkanOnly: false
INFO         |     useDedicatedAllocations: false
INFO         |     guestVulkanMaxApiVersion: 1.3.0
INFO         |     enableProtectedMemoryEmulation: false
INFO         | Graphics Adapter Vendor Google (Google Inc.)
INFO         | Graphics Adapter Android Emulator OpenGL ES Translator (Google SwiftShader)
INFO         | Graphics API Version OpenGL ES 3.0 (OpenGL ES 3.0 SwiftShader 4.0.0.1)
INFO         | Graphics API Extensions GL_OES_EGL_sync GL_OES_EGL_image GL_OES_EGL_image_external GL_OES_depth24 GL_OES_depth32 GL_OES_element_index_uint GL_OES_texture_float GL_OES_texture_float_linear GL_OES_compressed_paletted_texture GL_OES_compressed_ETC1_RGB8_texture GL_OES_depth_texture GL_OES_texture_half_float GL_OES_texture_half_float_linear GL_OES_packed_depth_stencil GL_OES_vertex_half_float GL_OES_standard_derivatives GL_OES_texture_npot GL_OES_rgb8_rgba8 GL_EXT_color_buffer_float GL_EXT_color_buffer_half_float GL_EXT_texture_format_BGRA8888 GL_APPLE_texture_format_BGRA8888 
INFO         | Graphics Device Extensions N/A
INFO         | Disabling sparse binding feature support
WARNING      | No adb private key exists
INFO         | Userspace boot properties:
INFO         |   androidboot.boot_devices=pci0000:00/0000:00:03.0 pci0000:00/0000:00:06.0
INFO         |   androidboot.dalvik.vm.heapsize=576m
INFO         |   androidboot.debug.hwui.renderer=skiagl
INFO         |   androidboot.debug.sf.nobootanimation=1
INFO         |   androidboot.hardware=ranchu
INFO         |   androidboot.hardware.gltransport=pipe
INFO         |   androidboot.hardware.vulkan=ranchu
INFO         |   androidboot.logcat=*:V
INFO         |   androidboot.opengles.version=196608
INFO         |   androidboot.qemu=1
INFO         |   androidboot.qemu.avd_name=gh_test
INFO         |   androidboot.qemu.camera_hq_edge_processing=0
INFO         |   androidboot.qemu.camera_protocol_ver=1
INFO         |   androidboot.qemu.cpuvulkan.version=4210688
INFO         |   androidboot.qemu.gltransport.drawFlushInterval=800
INFO         |   androidboot.qemu.gltransport.name=pipe
INFO         |   androidboot.qemu.hwcodec.avcdec=2
INFO         |   androidboot.qemu.hwcodec.hevcdec=2
INFO         |   androidboot.qemu.hwcodec.vpxdec=2
INFO         |   androidboot.qemu.settings.system.screen_off_timeout=2147483647
INFO         |   androidboot.qemu.skin=1080x2400
INFO         |   androidboot.qemu.virtiowifi=1
INFO         |   androidboot.qemu.vsync=60
INFO         |   androidboot.serialno=EMULATOR37X2X12X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7ff9f7401000 as it is in the protected range from 0x7ff8f7400000 to 0x7ff9f7600000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Successfully initialized netsim WiFi
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 27048 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 122
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 2825) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:39425 is gone due to Stream removed (CANCELLED)

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:packageDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:parseDebugLocalResources
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugAssets
> Task :app:compressDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:608:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792970387740.json

BUILD SUCCESSFUL in 2m 2s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 20s) ==
emulator can reach raw.githubusercontent.com after ~8s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3095)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tunnel up after ~4s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
tapped VPN consent at: 894 1519 (iter vpn-1)
vpn established after ~6s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::2/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::bfee:bc35:93e8:a645/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.113.3): 56(84) bytes.

--- 140.82.113.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
relay self-test PASS (real remote payload through the relay)
10-25 23:23:25.440  3095  4560 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=146 firstByteMs=320 checksums=0
10-25 23:23:25.605  3095  4597 D GhDiag  : relay_selftest ok=true stage=ok target=104.16.248.249:80 up=323 down=794 response=794 synAckMs=58 firstByteMs=141 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-25 23:23:25.874  3095  4615 D GhDiag  : flow_established 39ms
10-25 23:23:25.913  3095  4559 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:23:25.913  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=60
10-25 23:23:25.914  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=60
10-25 23:23:25.914  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=577
10-25 23:23:25.998  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=577
10-25 23:23:26.067  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:26.067  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.067  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:26.068  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.068  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.283  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=216
10-25 23:23:26.293  3095  4622 D GhDiag  : flow_established 28ms
10-25 23:23:26.294  3095  4623 D GhDiag  : flow_established 25ms
10-25 23:23:26.295  3095  4624 D GhDiag  : flow_established 35ms
10-25 23:23:26.298  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=231
10-25 23:23:26.298  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=230
10-25 23:23:26.424  3095  4559 D GhDiag  : flow_open 10.8.x.x:853
10-25 23:23:26.459  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=778
10-25 23:23:26.553  3095  4633 D GhDiag  : flow_established 63ms
10-25 23:23:26.610  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=151
10-25 23:23:26.740  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=128
10-25 23:23:26.936  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=188
10-25 23:23:27.007  3095  4618 D GhDiag  : flow_closed reason=upstream_eof up=517 down=0 ms=1186
10-25 23:23:27.115  3095  4620 D GhDiag  : flow_closed reason=upstream_eof up=517 down=0 ms=1307
10-25 23:23:27.215  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=274
10-25 23:23:27.468  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=245
10-25 23:23:27.473  3095  4559 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:23:27.597  3095  4665 D GhDiag  : flow_established 2ms
10-25 23:23:27.679  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:27.710  3095  4699 D GhDiag  : flow_established 9ms
10-25 23:23:27.797  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=134
10-25 23:23:27.944  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=146
10-25 23:23:28.252  3095  4559 D GhDiag  : flow_open 74.125.x.x:443
10-25 23:23:28.259  3095  4559 D GhDiag  : flow_open 74.125.x.x:443
10-25 23:23:28.313  3095  4717 D GhDiag  : flow_established 14ms
10-25 23:23:28.317  3095  4718 D GhDiag  : flow_established 17ms
10-25 23:23:28.956  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=414
10-25 23:23:28.974  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:28.991  3095  4732 D GhDiag  : flow_established 7ms
10-25 23:23:29.223  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=249
10-25 23:23:29.249  3095  4559 D GhDiag  : flow_open 142.250.x.x:443
10-25 23:23:29.508  3095  4758 D GhDiag  : flow_established 23ms
10-25 23:23:29.944  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:29.954  3095  4787 D GhDiag  : flow_established 1ms
10-25 23:23:30.116  3095  4558 D GhDiag  : stats t=5s packets=145 tcp=113 dns53=10 otherUdp=12 activeTcp=9 flowsOpened=16 flowsEstablished=16 connectFailures=0 retransmits=0 appUp=38575 appDown=30180 probeUp=184 probeDown=1196 probeFlows=2 dnsOk=10 dnsFail=0 state=VERIFIED ipv6=tunneled
10-25 23:23:30.126  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:30.130  3095  4796 D GhDiag  : flow_established 3ms
10-25 23:23:30.486  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=230
10-25 23:23:30.539  3095  4566 D GhDiag  : flow_closed reason=half_close_complete up=91 down=402 ms=5424
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 23:23:18.291  3095  3095 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 23:23:18.291  3095  3095 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 23:23:18.755  3095  3095 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 23:23:18.825  3095  3095 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:23:18.826  3095  3095 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:23:18.826  3095  3095 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 23:23:18.967  3095  3095 D GhDiag  : connect: core.start=true 
10-25 23:23:25.110  3095  3095 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 dns=10.8.0.1 mtu=1500
10-25 23:23:25.115  3095  4560 D GhDiag  : flow_open 1.1.x.x:80
10-25 23:23:25.206  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-25 23:23:25.210  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-25 23:23:25.210  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:23:25.210  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:23:25.257  3095  4567 D GhDiag  : flow_established 3ms
10-25 23:23:25.440  3095  4560 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=146 firstByteMs=320 checksums=0
10-25 23:23:25.458  3095  4597 D GhDiag  : selftest 1.1.1.1:80 failed at syn_ack: bad_ack_1477468113_expected_1191517255
10-25 23:23:25.463  3095  4597 D GhDiag  : flow_open 104.16.x.x:80
10-25 23:23:25.475  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=64
10-25 23:23:25.475  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=64
10-25 23:23:25.476  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=64
10-25 23:23:25.476  3095  4559 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-25 23:23:25.476  3095  4559 D GhDiag  : flow_open fd00:1:…:853
10-25 23:23:25.476  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=65
10-25 23:23:25.515  3095  4598 D GhDiag  : flow_established 6ms
10-25 23:23:25.518  3095  4599 D GhDiag  : flow_established 2ms
10-25 23:23:25.543  3095  4559 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:23:25.543  3095  4559 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=290
10-25 23:23:25.546  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:23:25.585  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:23:25.585  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-25 23:23:25.585  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-25 23:23:25.605  3095  4597 D GhDiag  : relay_selftest ok=true stage=ok target=104.16.248.249:80 up=323 down=794 response=794 synAckMs=58 firstByteMs=141 checksums=0
10-25 23:23:25.808  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:25.808  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:25.808  3095  4559 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:23:25.808  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:25.821  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:25.821  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:23:25.821  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:23:25.821  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:23:25.822  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:23:25.822  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:23:25.874  3095  4616 D GhDiag  : flow_established 16ms
10-25 23:23:25.874  3095  4615 D GhDiag  : flow_established 39ms
10-25 23:23:25.913  3095  4559 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:23:25.913  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=60
10-25 23:23:25.914  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=60
10-25 23:23:25.914  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=577
10-25 23:23:25.998  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=577
10-25 23:23:26.067  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:26.067  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.067  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:26.068  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.068  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.283  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=216
10-25 23:23:26.293  3095  4622 D GhDiag  : flow_established 28ms
10-25 23:23:26.294  3095  4623 D GhDiag  : flow_established 25ms
10-25 23:23:26.295  3095  4624 D GhDiag  : flow_established 35ms
10-25 23:23:26.298  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=231
10-25 23:23:26.298  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=230
10-25 23:23:26.424  3095  4559 D GhDiag  : flow_open 10.8.x.x:853
10-25 23:23:26.459  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=778
10-25 23:23:26.553  3095  4633 D GhDiag  : flow_established 63ms
10-25 23:23:26.610  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=151
10-25 23:23:26.740  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=128
10-25 23:23:26.936  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=188
10-25 23:23:27.007  3095  4618 D GhDiag  : flow_closed reason=upstream_eof up=517 down=0 ms=1186
10-25 23:23:27.115  3095  4620 D GhDiag  : flow_closed reason=upstream_eof up=517 down=0 ms=1307
10-25 23:23:27.215  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=274
10-25 23:23:27.468  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=245
10-25 23:23:27.473  3095  4559 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:23:27.597  3095  4665 D GhDiag  : flow_established 2ms
10-25 23:23:27.679  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:27.710  3095  4699 D GhDiag  : flow_established 9ms
10-25 23:23:27.797  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=134
10-25 23:23:27.944  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=146
10-25 23:23:28.252  3095  4559 D GhDiag  : flow_open 74.125.x.x:443
10-25 23:23:28.259  3095  4559 D GhDiag  : flow_open 74.125.x.x:443
10-25 23:23:28.313  3095  4717 D GhDiag  : flow_established 14ms
10-25 23:23:28.317  3095  4718 D GhDiag  : flow_established 17ms
10-25 23:23:28.956  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=414
10-25 23:23:28.974  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:28.991  3095  4732 D GhDiag  : flow_established 7ms
10-25 23:23:29.223  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=249
10-25 23:23:29.249  3095  4559 D GhDiag  : flow_open 142.250.x.x:443
10-25 23:23:29.508  3095  4758 D GhDiag  : flow_established 23ms
10-25 23:23:29.944  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:29.954  3095  4787 D GhDiag  : flow_established 1ms
10-25 23:23:30.116  3095  4558 D GhDiag  : stats t=5s packets=145 tcp=113 dns53=10 otherUdp=12 activeTcp=9 flowsOpened=16 flowsEstablished=16 connectFailures=0 retransmits=0 appUp=38575 appDown=30180 probeUp=184 probeDown=1196 probeFlows=2 dnsOk=10 dnsFail=0 state=VERIFIED ipv6=tunneled
10-25 23:23:30.126  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:30.130  3095  4796 D GhDiag  : flow_established 3ms
10-25 23:23:30.486  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=230
10-25 23:23:30.539  3095  4566 D GhDiag  : flow_closed reason=half_close_complete up=91 down=402 ms=5424
10-25 23:23:30.638  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=140
10-25 23:23:30.640  3095  4566 D GhDiag  : flow_closed reason=half_close_complete up=93 down=794 ms=5177
10-25 23:23:30.658  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:30.776  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:30.828  3095  4820 D GhDiag  : flow_established 37ms
10-25 23:23:30.830  3095  4816 D GhDiag  : flow_established 100ms
10-25 23:23:31.069  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=158
10-25 23:23:31.299  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=200
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
  522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{f8edc5f com.google.android.as/10125} BLOCKED
10-25 23:23:13.431   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{772f6ac com.google.android.gm/10142} BLOCKED
10-25 23:23:13.431   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{8239f75 com.google.android.dialer/10128} BLOCKED
10-25 23:23:13.431   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{b3ebb0a com.google.android.contacts/10155} BLOCKED
10-25 23:23:13.431   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{a6edf7b com.google.android.partnersetup/10124} BLOCKED
10-25 23:23:13.431   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{d6ed198 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 23:23:13.431   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{f9bbdf1 com.google.android.cellbroadcastreceiver/10188} BLOCKED
10-25 23:23:13.713   522   540 W ziparchive: Unable to open '/data/app/~~e8cmNWdUh5w9j3dcm9z4nw==/com.ghprotocol.app-t9WKmKtR075zd7o_uFW3iA==/base.dm': No such file or directory
10-25 23:23:13.713   522   540 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +4s123ms
10-25 23:23:13.833   522   536 W InputManager-JNI: Input channel object 'c498414 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 23:23:13.841   522  2440 D CoreBackPreview: Window{c498414 u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-25 23:23:14.072  3095  3353 W .ghprotocol.app: Verification of void kotlin.io.FilesKt__FileReadWriteKt.writeTextImpl(java.io.OutputStream, java.lang.String, java.nio.charset.Charset) took 108.228ms (1515.31 bytecodes/s) (4464B approximate peak alloc)
10-25 23:23:15.563   522   902 I ImeTracker: com.ghprotocol.app:1a132d43: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 23:23:15.563   522   902 I ImeTracker: com.ghprotocol.app:1a132d43: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 23:23:15.573  1531  1531 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 23:23:15.662   522  2443 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{7a02d49 com.google.android.settings.intelligence/10118} BLOCKED
10-25 23:23:16.005  1624  1624 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 23:23:16.588  1624  1624 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 23:23:16.594  1624  2384 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 23:23:16.594  1624  2384 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 23:23:16.598  3095  3847 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 23:23:16.854   522  2569 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{e27bb23 com.google.android.gm/10142} BLOCKED
10-25 23:23:18.177   522   590 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 23:23:18.177   830   875 V WindowManagerShell: Transition requested: android.os.BinderProxy@c8b4c9e TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=41158 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@8dbf37f} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{d118f4c com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:23:18.291  3095  3095 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 23:23:18.291  3095  3095 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 23:23:18.347  4063  4063 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 23:23:18.351  4063  4063 I AndroidRuntime: Using default boot image
10-25 23:23:18.351  4063  4063 I AndroidRuntime: Leaving lock profiling enabled
10-25 23:23:18.531  4063  4063 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 23:23:18.608  4124  4124 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:23:18.608  4124  4124 W libxraycore.so: type=1400 audit(0.0:19): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:23:18.608  4124  4124 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:23:18.608  4124  4124 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:23:18.755  3095  3095 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 23:23:18.825  3095  3095 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:23:18.826  3095  3095 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:23:18.826  3095  3095 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 23:23:18.967  3095  3095 D GhDiag  : connect: core.start=true 
10-25 23:23:19.006  1397  4159 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 23:23:19.031  1450  3623 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 23:23:19.141   522  2444 D CoreBackPreview: Window{67591fe u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@3e2383e, mPriority=0, mIsAnimationCallback=false}
10-25 23:23:19.565  4063  4063 D AndroidRuntime: Shutting down VM
10-25 23:23:20.008  4162  4162 W libxraycore.so: type=1400 audit(0.0:32): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=56401 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 23:23:20.417   522   620 I InputDispatcher: 72f441f com.ghprotocol.app/com.ghprotocol.app.MainActivity (server) spent 2208ms processing FocusEvent(hasFocus=false)
10-25 23:23:20.427   830   875 V WindowManagerShell: onTransitionReady android.os.BinderProxy@c8b4c9e: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a2a5b68 u0 com.ghprotocol.app/.MainActivity)/@0x36d377 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{535bf5b u0 com.ghprotocol.app/.MainActivity)/@0xd07be4 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:23:20.428   522   540 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +2s260ms
10-25 23:23:20.428   522   540 V WindowManager: Sent Transition #7 createdAt=10-25 23:23:18.169 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=41158 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{ed90a27 Task{8cbdb27 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{dcf473f com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:23:20.434   830   875 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a2a5b68 u0 com.ghprotocol.app/.MainActivity)/@0x36d377 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{535bf5b u0 com.ghprotocol.app/.MainActivity)/@0xd07be4 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:23:20.434   830   875 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a2a5b68 u0 com.ghprotocol.app/.MainActivity)/@0x36d377 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{535bf5b u0 com.ghprotocol.app/.MainActivity)/@0xd07be4 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:23:20.448   522   540 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a2a5b68 u0 com.ghprotocol.app/.MainActivity)/@0x7f0a899 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{535bf5b u0 com.ghprotocol.app/.MainActivity)/@0xdbf9de0 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:23:20.675   830   875 V WindowManagerShell: Transition requested: android.os.BinderProxy@ac22b81 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=43495 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@4b40426} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{54d8867 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:23:20.949   522  2569 I ImeTracker: com.ghprotocol.app:29fe3a5e: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 23:23:20.951  3095  3125 I .ghprotocol.app: Background concurrent copying GC freed 119515(5981KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 7015KB/13MB, paused 20us,13us total 458.810ms
10-25 23:23:20.954   522  2569 I ImeTracker: com.ghprotocol.app:29fe3a5e: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 23:23:20.961  1531  1531 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 23:23:21.254  4323  4323 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 23:23:21.261  4323  4323 I AndroidRuntime: Using default boot image
10-25 23:23:21.264  4323  4323 I AndroidRuntime: Leaving lock profiling enabled
10-25 23:23:21.540  4323  4323 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 23:23:21.686   522  2445 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 23:23:21.686   522  2445 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 23:23:21.686   522  2445 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 23:23:22.255   522   540 V WindowManager: Sent Transition #8 createdAt=10-25 23:23:20.506 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=43495 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{ed90a27 Task{8cbdb27 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{2ad52c5 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:23:23.290  4323  4323 D AndroidRuntime: Shutting down VM
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{fa9f9c4 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{71140ad com.google.android.apps.messaging/10130} BLOCKED
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{6db6fe2 com.android.camera2/10144} BLOCKED
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{251af73 com.google.android.gm/10142} BLOCKED
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{62eee30 com.google.android.devicelockcontroller/10180} BLOCKED
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{7ae3aa9 com.google.android.rkpdapp/10189} BLOCKED
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{2c4a82e com.google.android.settings.intelligence/10118} BLOCKED
10-25 23:23:24.166   522   574 I AppsFilter: interaction: PackageSetting{32d3280 com.ghprotocol.app/10192} -> PackageSetting{bb16adb com.google.android.projection.gearhead/10123} BLOCKED
10-25 23:23:24.597   522  1894 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 23:23:24.866   522   537 I ImeTracker: com.ghprotocol.app:684fb35f: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 23:23:24.866   522   537 I ImeTracker: com.ghprotocol.app:684fb35f: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 23:23:24.870  1531  1531 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 23:23:24.877   522   537 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 23:23:25.109   522  1724 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 23:23:25.110  3095  3095 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 dns=10.8.0.1 mtu=1500
10-25 23:23:25.115  3095  4560 D GhDiag  : flow_open 1.1.x.x:80
10-25 23:23:25.206  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-25 23:23:25.210  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-25 23:23:25.210  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:23:25.210  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:23:25.257  3095  4567 D GhDiag  : flow_established 3ms
10-25 23:23:25.440  3095  4560 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=146 firstByteMs=320 checksums=0
10-25 23:23:25.458  3095  4597 D GhDiag  : selftest 1.1.1.1:80 failed at syn_ack: bad_ack_1477468113_expected_1191517255
10-25 23:23:25.463  3095  4597 D GhDiag  : flow_open 104.16.x.x:80
10-25 23:23:25.475  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=64
10-25 23:23:25.475  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=64
10-25 23:23:25.476  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=64
10-25 23:23:25.476  3095  4559 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-25 23:23:25.476  3095  4559 D GhDiag  : flow_open fd00:1:…:853
10-25 23:23:25.476  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=65
10-25 23:23:25.515  3095  4598 D GhDiag  : flow_established 6ms
10-25 23:23:25.518  3095  4599 D GhDiag  : flow_established 2ms
10-25 23:23:25.543  3095  4559 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:23:25.543  3095  4559 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=290
10-25 23:23:25.546  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:23:25.585  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:23:25.585  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-25 23:23:25.585  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-25 23:23:25.605  3095  4597 D GhDiag  : relay_selftest ok=true stage=ok target=104.16.248.249:80 up=323 down=794 response=794 synAckMs=58 firstByteMs=141 checksums=0
10-25 23:23:25.808  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:25.808  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:25.808  3095  4559 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:23:25.808  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:25.821  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:25.821  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:23:25.821  3095  4559 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:23:25.821  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:23:25.822  3095  4559 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:23:25.822  3095  4559 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:23:25.874  3095  4616 D GhDiag  : flow_established 16ms
10-25 23:23:25.874  3095  4615 D GhDiag  : flow_established 39ms
10-25 23:23:25.913  3095  4559 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:23:25.913  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=60
10-25 23:23:25.914  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=60
10-25 23:23:25.914  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=577
10-25 23:23:25.998  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=577
10-25 23:23:26.067  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:26.067  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.067  3095  4559 D GhDiag  : tun v6 proto=6 dst=2607:f8b0:…:443 len=80
10-25 23:23:26.068  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.068  3095  4559 D GhDiag  : flow_open 2607:f8b0:…:443
10-25 23:23:26.259  3095  3124 I .ghprotocol.app: Compiler allocated 4270KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-25 23:23:26.283  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=216
10-25 23:23:26.293  3095  4622 D GhDiag  : flow_established 28ms
10-25 23:23:26.294  3095  4623 D GhDiag  : flow_established 25ms
10-25 23:23:26.295  3095  4624 D GhDiag  : flow_established 35ms
10-25 23:23:26.298  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=231
10-25 23:23:26.298  3095  4559 D GhDiag  : flow_closed reason=client_rst up=0 down=0 ms=230
10-25 23:23:26.424  3095  4559 D GhDiag  : flow_open 10.8.x.x:853
10-25 23:23:26.459  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=778
10-25 23:23:26.553  3095  4633 D GhDiag  : flow_established 63ms
10-25 23:23:26.610  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=151
10-25 23:23:26.657  3095  3125 I .ghprotocol.app: Background young concurrent copying GC freed 108329(6406KB) AllocSpace objects, 2(40KB) LOS objects, 29% free, 9875KB/13MB, paused 2.818ms,25us total 230.621ms
10-25 23:23:26.740  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=128
10-25 23:23:26.936  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=188
10-25 23:23:27.007  3095  4618 D GhDiag  : flow_closed reason=upstream_eof up=517 down=0 ms=1186
10-25 23:23:27.115  3095  4620 D GhDiag  : flow_closed reason=upstream_eof up=517 down=0 ms=1307
10-25 23:23:27.215  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=274
10-25 23:23:27.272  3095  3124 I .ghprotocol.app: Compiler allocated 4270KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-25 23:23:27.462  3095  3125 I .ghprotocol.app: Background young concurrent copying GC freed 96874(8415KB) AllocSpace objects, 0(0B) LOS objects, 42% free, 9603KB/16MB, paused 23us,10us total 243.007ms
10-25 23:23:27.468  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=245
10-25 23:23:27.473  3095  4559 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:23:27.597  3095  4665 D GhDiag  : flow_established 2ms
10-25 23:23:27.679  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:27.710  3095  4699 D GhDiag  : flow_established 9ms
10-25 23:23:27.797  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=134
10-25 23:23:27.944  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=146
10-25 23:23:28.252  3095  4559 D GhDiag  : flow_open 74.125.x.x:443
10-25 23:23:28.259  3095  4559 D GhDiag  : flow_open 74.125.x.x:443
10-25 23:23:28.313  3095  4717 D GhDiag  : flow_established 14ms
10-25 23:23:28.317  3095  4718 D GhDiag  : flow_established 17ms
10-25 23:23:28.948  3095  3125 I .ghprotocol.app: Background concurrent copying GC freed 113088(9127KB) AllocSpace objects, 12(240KB) LOS objects, 49% free, 8455KB/16MB, paused 10.567ms,9us total 285.687ms
10-25 23:23:28.956  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=414
10-25 23:23:28.974  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:28.991  3095  4732 D GhDiag  : flow_established 7ms
10-25 23:23:29.223  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=249
10-25 23:23:29.249  3095  4559 D GhDiag  : flow_open 142.250.x.x:443
10-25 23:23:29.508  3095  4758 D GhDiag  : flow_established 23ms
10-25 23:23:29.684  3095  3125 I .ghprotocol.app: Background young concurrent copying GC freed 97366(8425KB) AllocSpace objects, 0(0B) LOS objects, 9% free, 15MB/16MB, paused 18us,26us total 356.362ms
10-25 23:23:29.944  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:29.954  3095  4787 D GhDiag  : flow_established 1ms
10-25 23:23:30.116  3095  4558 D GhDiag  : stats t=5s packets=145 tcp=113 dns53=10 otherUdp=12 activeTcp=9 flowsOpened=16 flowsEstablished=16 connectFailures=0 retransmits=0 appUp=38575 appDown=30180 probeUp=184 probeDown=1196 probeFlows=2 dnsOk=10 dnsFail=0 state=VERIFIED ipv6=tunneled
10-25 23:23:30.126  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:30.130  3095  4796 D GhDiag  : flow_established 3ms
10-25 23:23:30.486  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=230
10-25 23:23:30.530  3095  3125 I .ghprotocol.app: Background young concurrent copying GC freed 98614(8560KB) AllocSpace objects, 0(0B) LOS objects, 38% free, 10MB/16MB, paused 21us,15us total 249.628ms
10-25 23:23:30.539  3095  4566 D GhDiag  : flow_closed reason=half_close_complete up=91 down=402 ms=5424
10-25 23:23:30.638  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=140
10-25 23:23:30.640  3095  4566 D GhDiag  : flow_closed reason=half_close_complete up=93 down=794 ms=5177
10-25 23:23:30.658  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:30.776  3095  4559 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:23:30.828  3095  4820 D GhDiag  : flow_established 37ms
10-25 23:23:30.830  3095  4816 D GhDiag  : flow_established 100ms
10-25 23:23:31.069  3095  4611 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=158

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
