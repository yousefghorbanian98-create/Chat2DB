## gh-protocol E2E log — 2026-10-25T15:53:15Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T15:51:53Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 15:48 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 15:52 .
drwxr-xr-x 3 runner runner 4096 Oct 25 15:52 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 15:52 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 15:52 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2826
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
WARNING: cannnot unmap ptr 0x7fbcf7001000 as it is in the protected range from 0x7fbbf7000000 to 0x7fbcf7200000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Successfully initialized netsim WiFi
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 27003 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
INFO         | Wait for emulator (pid 2826) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:44957 is gone due to Stream removed (CANCELLED)

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
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mapDebugSourceSetPaths
> Task :app:javaPreCompileDebug
> Task :app:checkDebugAarMetadata
> Task :app:mergeDebugShaders
> Task :app:desugarDebugFileDependencies
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugAssets
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:compressDebugAssets
> Task :app:mergeDebugNativeLibs
> Task :app:mergeLibDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792943368876.json

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
emulator can reach raw.githubusercontent.com after ~12s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3254)
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
    inet6 fd00:1::1/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::fbf4:ad8c:af61:f455/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.112.3): 56(84) bytes.

--- 140.82.112.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
--------- beginning of main
10-25 15:53:02.164  3254  3254 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 15:53:02.164  3254  3254 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 15:53:02.455  3254  3254 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 15:53:02.481  3254  3254 D GhDiag  : connect: config written bytes=5112 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 15:53:02.676  3254  3254 D GhDiag  : connect: core.start=true 
10-25 15:53:07.625  3254  3254 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 15:53:07.681  3254  3254 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@cb55a48} — relay loop started
10-25 15:53:08.024  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:53:08.024  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:53:08.131  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.165  3254  3393 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (111ms)
10-25 15:53:08.326  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:08.326  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 15:53:08.333  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 15:53:08.342  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.491  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:53:08.502  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:53:08.539  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:53:08.541  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:53:08.683  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 15:53:08.691  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 15:53:08.771  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.995  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 15:53:09.033  3254  4667 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 15:53:09.035  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 15:53:09.035  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 15:53:09.347  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:09.636  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:10.183  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 15:53:10.184  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=889
10-25 15:53:10.371  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:10.392  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 15:53:10.809  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=889
10-25 15:53:11.020  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 15:53:02.164  3254  3254 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 15:53:02.164  3254  3254 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 15:53:02.455  3254  3254 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 15:53:02.481  3254  3254 D GhDiag  : connect: config written bytes=5112 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 15:53:02.676  3254  3254 D GhDiag  : connect: core.start=true 
10-25 15:53:07.625  3254  3254 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 15:53:07.681  3254  3254 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@cb55a48} — relay loop started
10-25 15:53:08.024  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:53:08.024  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:53:08.131  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.165  3254  3393 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (111ms)
10-25 15:53:08.326  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:08.326  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 15:53:08.333  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 15:53:08.342  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.491  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:53:08.502  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:53:08.539  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:53:08.541  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:53:08.683  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 15:53:08.691  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 15:53:08.771  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.995  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 15:53:09.033  3254  4667 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 15:53:09.035  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 15:53:09.035  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 15:53:09.347  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:09.636  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:10.183  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 15:53:10.184  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=889
10-25 15:53:10.371  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:10.392  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 15:53:10.809  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=889
10-25 15:53:11.020  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
49.244   520   798 I SdkSandboxManager: No SDKs used. Skipping SDK data reconcilation for CallingInfo{mUid=10192, mPackageName='com.ghprotocol.app, mAppProcessToken='null'}
10-25 15:52:50.003  1044  1044 D CarrierSvcBindHelper: onPackageAdded: com.ghprotocol.app
10-25 15:52:50.167  1044  1313 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 15:52:50.393  1044  1044 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-25 15:52:50.560  1044  1313 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 15:52:51.367   830   830 I SafetyLabelChangedBroadcastReceiver: received broadcast packageName: com.ghprotocol.app, current user: UserHandle{0}, packageChangeEvent: NEW_INSTALL, intent user: UserHandle{0}
10-25 15:52:51.643  1094  1156 I Launcher.IconCache: Database bulk icon loading failed, using fallback bulk icon loading for: ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 15:52:53.758   520  2181 V SplashScreenExceptionList: SplashScreen checking exception for package com.ghprotocol.app (target sdk:35) -> false
10-25 15:52:53.766   520  2181 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 15:52:53.768   828   867 V WindowManagerShell: Transition requested: android.os.BinderProxy@2e2a87b TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=34035 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@3f96698} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{32ef1 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:52:53.929   520  2398 D CoreBackPreview: Window{a48fc69 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@3e45852, mPriority=0, mIsAnimationCallback=false}
10-25 15:52:54.135   520   537 V WindowManager: Sent Transition #6 createdAt=10-25 15:52:53.750 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=34035 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{eed396f Task{8b35856 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{d5b767c com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:52:54.135   520   537 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{eed396f Task{8b35856 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x488e349 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{df36b05 Task{87c1d25 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x781737e sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:52:54.433   520   550 I ActivityManager: Start proc 3254:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 15:52:54.640  3254  3254 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 15:52:54.660  1579  1579 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 15:52:54.714  3254  3254 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 15:52:54.716  3254  3254 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 15:52:54.716  3254  3254 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 15:52:54.817  3254  3254 W ziparchive: Unable to open '/data/app/~~gkeX8kyRB2lM-l5pOOTM5w==/com.ghprotocol.app-RaS1kgiBSWVy_sZBfS-4hA==/base.dm': No such file or directory
10-25 15:52:54.817  3254  3254 W ziparchive: Unable to open '/data/app/~~gkeX8kyRB2lM-l5pOOTM5w==/com.ghprotocol.app-RaS1kgiBSWVy_sZBfS-4hA==/base.dm': No such file or directory
10-25 15:52:55.179  3254  3254 D nativeloader: Configuring clns-6 for other apk /data/app/~~gkeX8kyRB2lM-l5pOOTM5w==/com.ghprotocol.app-RaS1kgiBSWVy_sZBfS-4hA==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~gkeX8kyRB2lM-l5pOOTM5w==/com.ghprotocol.app-RaS1kgiBSWVy_sZBfS-4hA==/lib/x86_64:/data/app/~~gkeX8kyRB2lM-l5pOOTM5w==/com.ghprotocol.app-RaS1kgiBSWVy_sZBfS-4hA==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 15:52:55.188  3254  3254 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 15:52:55.188  3254  3254 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 15:52:55.339  1579  1579 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 15:52:55.340  1579  2707 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 15:52:55.341  1579  2707 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 15:52:55.611   520  1595 D CoreBackPreview: Window{19338c1 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@4bf4074, mPriority=0, mIsAnimationCallback=false}
10-25 15:52:55.826  3254  3254 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 15:52:55.826  3254  3254 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 15:52:55.826  3254  3254 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 15:52:55.827  3254  3254 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 15:52:55.827  3254  3254 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 15:52:55.827  3254  3254 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 15:52:55.827  3254  3254 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{e249324 com.google.android.youtube/10139} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{c3fce8d com.google.android.googlequicksearchbox/10131} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{6281842 com.google.android.as/10126} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{b82a053 com.google.android.gm/10142} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{6a9bd90 com.google.android.devicelockcontroller/10173} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{b67c689 com.google.android.dialer/10128} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{a3768e com.google.android.contacts/10153} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{38ceeaf com.google.android.partnersetup/10124} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{e1522bc com.google.android.apps.youtube.music/10156} BLOCKED
10-25 15:52:56.337   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{8fd4245 com.google.android.inputmethod.latin/10141} BLOCKED
10-25 15:52:57.025   520   537 W ziparchive: Unable to open '/data/app/~~gkeX8kyRB2lM-l5pOOTM5w==/com.ghprotocol.app-RaS1kgiBSWVy_sZBfS-4hA==/base.dm': No such file or directory
10-25 15:52:57.032   520   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s286ms
10-25 15:52:57.076   520  2227 W InputManager-JNI: Input channel object 'a48fc69 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 15:52:57.077   520  1939 D CoreBackPreview: Window{a48fc69 u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-25 15:52:57.173   520  1595 I ImeTracker: com.ghprotocol.app:9458ab39: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 15:52:57.173   520  1595 I ImeTracker: com.ghprotocol.app:9458ab39: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 15:52:57.196  1500  1500 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 15:52:58.722   520  2235 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{bd20436 com.google.android.gm/10142} BLOCKED
10-25 15:53:00.834  1398  3481 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 15:53:00.908  1443  3204 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 15:53:00.970   520  1084 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{adb1691 com.google.android.settings.intelligence/10118} BLOCKED
10-25 15:53:00.979   520  2401 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{ecb57d7 com.google.android.settings.intelligence/10118} BLOCKED
10-25 15:53:01.191  3254  4146 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 15:53:02.012   520   912 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 15:53:02.015   828   867 V WindowManagerShell: Transition requested: android.os.BinderProxy@7f35a80 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=42287 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@730b8b9} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{1d34fe com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:53:02.144  4208  4208 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 15:53:02.150  4208  4208 I AndroidRuntime: Using default boot image
10-25 15:53:02.151  4208  4208 I AndroidRuntime: Leaving lock profiling enabled
10-25 15:53:02.164  3254  3254 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 15:53:02.164  3254  3254 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 15:53:02.231  4228  4228 W libxraycore.so: type=1400 audit(0.0:17): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 15:53:02.235  4228  4228 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 15:53:02.244  4208  4208 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 15:53:02.235  4228  4228 W libxraycore.so: type=1400 audit(0.0:19): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 15:53:02.455  3254  3254 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 15:53:02.481  3254  3254 D GhDiag  : connect: config written bytes=5112 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 15:53:02.676  3254  3254 D GhDiag  : connect: core.start=true 
10-25 15:53:02.691   520  2396 D CoreBackPreview: Window{e6d4e4b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@e3767d5, mPriority=0, mIsAnimationCallback=false}
10-25 15:53:03.296  4208  4208 D AndroidRuntime: Shutting down VM
10-25 15:53:03.760   828   867 V WindowManagerShell: onTransitionReady android.os.BinderProxy@7f35a80: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d0a0bf0 u0 com.ghprotocol.app/.MainActivity)/@0xa03c5f1 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{7767271 u0 com.ghprotocol.app/.MainActivity)/@0x350e5d6 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:53:03.760   828   867 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d0a0bf0 u0 com.ghprotocol.app/.MainActivity)/@0xa03c5f1 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{7767271 u0 com.ghprotocol.app/.MainActivity)/@0x350e5d6 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:53:03.760   828   867 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d0a0bf0 u0 com.ghprotocol.app/.MainActivity)/@0xa03c5f1 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{7767271 u0 com.ghprotocol.app/.MainActivity)/@0x350e5d6 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:53:03.755  4294  4294 W libxraycore.so: type=1400 audit(0.0:32): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=56823 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 15:53:03.772   520   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s740ms
10-25 15:53:03.773   520   537 V WindowManager: Sent Transition #7 createdAt=10-25 15:53:02.007 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=42287 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{eed396f Task{8b35856 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{8d7d7a9 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:53:03.773   520   537 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d0a0bf0 u0 com.ghprotocol.app/.MainActivity)/@0x9dcb3da sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{7767271 u0 com.ghprotocol.app/.MainActivity)/@0xe2db985 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:53:03.959   828   867 V WindowManagerShell: Transition requested: android.os.BinderProxy@b02f8c8 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=44124 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@ac10d61} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{4c7086 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:53:04.307   520  2396 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 15:53:04.308   520  2396 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 15:53:04.308   520  2396 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 15:53:04.854  4500  4500 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 15:53:04.858  4500  4500 I AndroidRuntime: Using default boot image
10-25 15:53:04.858  4500  4500 I AndroidRuntime: Leaving lock profiling enabled
10-25 15:53:04.989   520   537 V WindowManager: Sent Transition #8 createdAt=10-25 15:53:03.847 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=44124 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{eed396f Task{8b35856 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{992f3a0 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:53:05.243  4500  4500 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 15:53:05.765  3254  3301 I .ghprotocol.app: Background concurrent copying GC freed 112927(5657KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6955KB/13MB, paused 29us,10us total 1.031s
10-25 15:53:06.492  4500  4500 D AndroidRuntime: Shutting down VM
10-25 15:53:06.621   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{67b46f7 com.google.android.apps.messaging/10129} BLOCKED
10-25 15:53:06.621   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{c26a964 com.android.camera2/10146} BLOCKED
10-25 15:53:06.621   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{b6ac7cd com.google.android.gm/10142} BLOCKED
10-25 15:53:06.621   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{ae5b882 com.google.android.devicelockcontroller/10173} BLOCKED
10-25 15:53:06.621   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{8935b93 com.google.android.rkpdapp/10172} BLOCKED
10-25 15:53:06.621   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{356f7d0 com.google.android.settings.intelligence/10118} BLOCKED
10-25 15:53:06.621   520   572 I AppsFilter: interaction: PackageSetting{fbbfb7 com.ghprotocol.app/10192} -> PackageSetting{442a98d com.google.android.projection.gearhead/10123} BLOCKED
10-25 15:53:07.532   520  2233 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 15:53:07.611   520  2189 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 15:53:07.625  3254  3254 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 15:53:07.680   520  1694 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 15:53:07.681  3254  3254 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@cb55a48} — relay loop started
10-25 15:53:07.856   520  2396 I ImeTracker: com.ghprotocol.app:ad91afbd: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 15:53:07.856   520  2396 I ImeTracker: com.ghprotocol.app:ad91afbd: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 15:53:07.919  1500  1500 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 15:53:08.024  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:53:08.024  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:53:08.131  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.165  3254  3393 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (111ms)
10-25 15:53:08.240  3254  3300 I .ghprotocol.app: Compiler allocated 4115KB to compile void com.ghprotocol.app.ui.HomeScreenKt.WorldClassConnectHub(com.ghprotocol.app.ui.HomeUiState, com.ghprotocol.app.ui.HomeViewModel, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-25 15:53:08.326  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:08.326  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 15:53:08.333  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 15:53:08.342  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.491  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:53:08.502  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:53:08.539  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:53:08.541  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:53:08.683  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 15:53:08.691  3254  4618 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 15:53:08.771  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:08.995  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 15:53:09.033  3254  4667 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 15:53:09.035  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 15:53:09.035  3254  4618 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 15:53:09.347  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:09.636  3254  4618 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:53:10.183  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 15:53:10.184  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=889
10-25 15:53:10.371  3254  4618 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:53:10.392  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 15:53:10.809  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=889
10-25 15:53:11.020  3254  4618 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
