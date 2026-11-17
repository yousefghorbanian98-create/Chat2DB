## gh-protocol E2E log — 2026-11-17T15:03:33Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-11-17T14:52:20Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Nov 17 14:48 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Nov 17 14:53 .
drwxr-xr-x 3 runner runner 4096 Nov 17 14:53 ..
drwxr-xr-x 3 runner runner 4096 Nov 17 14:53 gh_test.avd
-rw-r--r-- 1 runner runner  115 Nov 17 14:53 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.13.0 (build_id 16740729) (CL:N/A)
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
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15982 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15982 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.13.db, detection is enabled for process: 3026
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
INFO         |   androidboot.serialno=EMULATOR37X2X13X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x719e27401000 as it is in the protected range from 0x719d27400000 to 0x719e27600000
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
INFO         | Boot completed in 35589 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 41
ERROR        | Failed to bind to texture: invalid color buffer.

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
> Task :app:preBuild UP-TO-DATE
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mapDebugSourceSetPaths
> Task :app:extractDeepLinksDebug
> Task :app:checkDebugAarMetadata
> Task :app:packageDebugResources
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:mergeDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:compressDebugAssets
> Task :app:mergeDebugResources
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:checkDebugDuplicateClasses
> Task :app:processDebugResources
> Task :app:mergeDebugNativeLibs
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1794926958119.json

BUILD SUCCESSFUL in 2m 44s
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
emulator can reach raw.githubusercontent.com after ~4s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3440)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       3440   338   14167876 184536 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp      130      0 10.0.2.16:45600         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:50166         172.217.112.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:50200         172.217.112.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:50150         172.217.112.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:54720         172.217.114.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:40978         172.217.114.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:50180         172.217.112.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:50134         172.217.112.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:50184         172.217.112.4:443       CLOSE_WAIT 
tcp6       0      0 ::ffff:127.0.0.1:35515  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:43057  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.16:60868  ::ffff:142.251.154.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:49784  ::ffff:192.179.17.2:443 CLOSE_WAIT 
tcp6       0      0 ::ffff:10.0.2.16:39996  ::ffff:142.251.183:5228 ESTABLISHED
tcp6       1      0 ::ffff:10.0.2.16:57282  ::ffff:74.125.132.1:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:47540  ::ffff:172.217.117.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:43730  ::ffff:172.253.155.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{95e4c23 u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{725b049 3440:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~b_ShfOTwlm3DzcUb7OOLzA==/com.ghprotocol.app-1NkBEUp8oI0B1tfAKDXQAw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.35 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
        backgroundColor=ff303030 statusBarColor=0 navigationBarColor=0
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-9m17s658ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{95e4c23 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{725b049 3440:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~b_ShfOTwlm3DzcUb7OOLzA==/com.ghprotocol.app-1NkBEUp8oI0B1tfAKDXQAw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.35 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      ResolvedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} s.2 ?fontWeightAdjustment}
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{6f8cbe1 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-9m22s476ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@101266703
  deepestLastOrientationSource=ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.35 fontWeightAdjustment=0}
  mLayoutSeq=86
  mCurrentFocus=Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{95e4c23 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{90bdfa5 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{fda83b9 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{921ee03 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{d6d86aa #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{45e9638 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{3a42762 u0 StatusBar}
    mFocusedWindow=Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{5dc5b2a u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=14220006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {14220000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=14220006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{3a42762 u0 StatusBar}
--
        mWindowContainer=Window{3a42762 u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=3a42762 StatusBar)/@0xb394c6a - animation-leash of insets_animation)/@0xf290bce
        mControlTarget=Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=7b063e2 InputMethod)/@0x4f0230 - animation-leash of insets_animation)/@0x566faef mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{7b063e2 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=7b063e2 InputMethod)/@0x4f0230 - animation-leash of insets_animation)/@0x566faef
        mControlTarget=Window{11bb156 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{826529b #3 type=undefined}
        (multi-window) Task{45e9638 #4 type=undefined}
        (fullscreen) Task{3b0b09e #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{725b049 3440:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6212
drwx------ 2 u0_a192 u0_a192    4096 2026-11-17 14:54 .
drwxrwx--x 3 u0_a192 u0_a192    4096 2026-11-17 14:54 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-11-17 14:54 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-11-17 14:54 geosite.dat
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
runtime config (first 1400 bytes):
core exit line:
GhDiag (connect-flow trace):
--------- beginning of main
11-17 14:54:13.056  3440  3440 D GhDiag  : connect: tap -> CHECKING (have sub=true)
11-17 14:54:13.056  3440  3440 D GhDiag  : connect: sub ok entries=3 -> PREPARING (core extract+version)
11-17 14:54:13.336  3440  3440 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
11-17 14:54:13.336  3440  3440 D GhDiag  : connect: FAILED — core unavailable/old (min=26.11.21)
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
d 2000 <<<<<<
11-17 14:56:39.058  6392  6392 I AndroidRuntime: Using default boot image
11-17 14:56:39.058  6392  6392 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:56:39.159  6392  6392 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:56:40.218  6392  6392 D AndroidRuntime: Shutting down VM
11-17 14:56:45.208  6415  6415 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:56:45.213  6415  6415 I AndroidRuntime: Using default boot image
11-17 14:56:45.213  6415  6415 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:56:45.307  6415  6415 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:56:46.373  6415  6415 D AndroidRuntime: Shutting down VM
11-17 14:56:51.386  6440  6440 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:56:51.391  6440  6440 I AndroidRuntime: Using default boot image
11-17 14:56:51.391  6440  6440 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:56:51.493  6440  6440 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:56:52.556  6440  6440 D AndroidRuntime: Shutting down VM
11-17 14:56:57.553  6463  6463 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:56:57.558  6463  6463 I AndroidRuntime: Using default boot image
11-17 14:56:57.558  6463  6463 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:56:57.656  6463  6463 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:56:58.718  6463  6463 D AndroidRuntime: Shutting down VM
11-17 14:57:03.693  6488  6488 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:03.698  6488  6488 I AndroidRuntime: Using default boot image
11-17 14:57:03.698  6488  6488 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:03.793  6488  6488 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:04.860  6488  6488 D AndroidRuntime: Shutting down VM
11-17 14:57:09.834  6520  6520 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:09.838  6520  6520 I AndroidRuntime: Using default boot image
11-17 14:57:09.838  6520  6520 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:09.935  6520  6520 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:11.015  6520  6520 D AndroidRuntime: Shutting down VM
11-17 14:57:15.996  6544  6544 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:16.000  6544  6544 I AndroidRuntime: Using default boot image
11-17 14:57:16.000  6544  6544 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:16.096  6544  6544 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:17.157  6544  6544 D AndroidRuntime: Shutting down VM
11-17 14:57:22.196  6572  6572 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:22.200  6572  6572 I AndroidRuntime: Using default boot image
11-17 14:57:22.200  6572  6572 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:22.298  6572  6572 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:23.371  6572  6572 D AndroidRuntime: Shutting down VM
11-17 14:57:28.366  6596  6596 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:28.370  6596  6596 I AndroidRuntime: Using default boot image
11-17 14:57:28.370  6596  6596 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:28.466  6596  6596 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:29.555  6596  6596 D AndroidRuntime: Shutting down VM
11-17 14:57:34.530  6629  6629 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:34.534  6629  6629 I AndroidRuntime: Using default boot image
11-17 14:57:34.534  6629  6629 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:34.640  6629  6629 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:35.719  6629  6629 D AndroidRuntime: Shutting down VM
11-17 14:57:40.696  6653  6653 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:40.700  6653  6653 I AndroidRuntime: Using default boot image
11-17 14:57:40.701  6653  6653 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:40.802  6653  6653 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:41.855  6653  6653 D AndroidRuntime: Shutting down VM
11-17 14:57:46.847  6676  6676 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:46.851  6676  6676 I AndroidRuntime: Using default boot image
11-17 14:57:46.851  6676  6676 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:46.952  6676  6676 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:48.025  6676  6676 D AndroidRuntime: Shutting down VM
11-17 14:57:53.034  6702  6702 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:53.038  6702  6702 I AndroidRuntime: Using default boot image
11-17 14:57:53.038  6702  6702 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:53.135  6702  6702 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:57:54.203  6702  6702 D AndroidRuntime: Shutting down VM
11-17 14:57:59.190  6725  6725 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:57:59.195  6725  6725 I AndroidRuntime: Using default boot image
11-17 14:57:59.195  6725  6725 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:57:59.291  6725  6725 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:00.361  6725  6725 D AndroidRuntime: Shutting down VM
11-17 14:58:05.340  6748  6748 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:05.344  6748  6748 I AndroidRuntime: Using default boot image
11-17 14:58:05.344  6748  6748 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:05.441  6748  6748 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:06.503  6748  6748 D AndroidRuntime: Shutting down VM
11-17 14:58:11.491  6771  6771 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:11.496  6771  6771 I AndroidRuntime: Using default boot image
11-17 14:58:11.496  6771  6771 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:11.591  6771  6771 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:12.651  6771  6771 D AndroidRuntime: Shutting down VM
11-17 14:58:17.630  6796  6796 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:17.634  6796  6796 I AndroidRuntime: Using default boot image
11-17 14:58:17.634  6796  6796 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:17.733  6796  6796 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:18.819  6796  6796 D AndroidRuntime: Shutting down VM
11-17 14:58:23.815  6822  6822 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:23.819  6822  6822 I AndroidRuntime: Using default boot image
11-17 14:58:23.819  6822  6822 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:23.919  6822  6822 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:25.002  6822  6822 D AndroidRuntime: Shutting down VM
11-17 14:58:29.984  6846  6846 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:29.989  6846  6846 I AndroidRuntime: Using default boot image
11-17 14:58:29.989  6846  6846 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:30.090  6846  6846 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:31.157  6846  6846 D AndroidRuntime: Shutting down VM
11-17 14:58:36.145  6901  6901 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:36.150  6901  6901 I AndroidRuntime: Using default boot image
11-17 14:58:36.150  6901  6901 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:36.251  6901  6901 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:37.308  6901  6901 D AndroidRuntime: Shutting down VM
11-17 14:58:42.284  6932  6932 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:42.288  6932  6932 I AndroidRuntime: Using default boot image
11-17 14:58:42.288  6932  6932 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:42.387  6932  6932 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:43.456  6932  6932 D AndroidRuntime: Shutting down VM
11-17 14:58:48.453  6961  6961 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:48.457  6961  6961 I AndroidRuntime: Using default boot image
11-17 14:58:48.457  6961  6961 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:48.555  6961  6961 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:49.634  6961  6961 D AndroidRuntime: Shutting down VM
11-17 14:58:54.642  6986  6986 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:58:54.646  6986  6986 I AndroidRuntime: Using default boot image
11-17 14:58:54.646  6986  6986 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:58:54.745  6986  6986 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:58:55.813  6986  6986 D AndroidRuntime: Shutting down VM
11-17 14:59:00.792  7010  7010 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:00.796  7010  7010 I AndroidRuntime: Using default boot image
11-17 14:59:00.796  7010  7010 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:00.894  7010  7010 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:01.948  7010  7010 D AndroidRuntime: Shutting down VM
11-17 14:59:06.925  7034  7034 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:06.929  7034  7034 I AndroidRuntime: Using default boot image
11-17 14:59:06.929  7034  7034 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:07.025  7034  7034 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:08.089  7034  7034 D AndroidRuntime: Shutting down VM
11-17 14:59:13.073  7057  7057 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:13.078  7057  7057 I AndroidRuntime: Using default boot image
11-17 14:59:13.078  7057  7057 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:13.175  7057  7057 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:14.221  7057  7057 D AndroidRuntime: Shutting down VM
11-17 14:59:19.189  7080  7080 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:19.193  7080  7080 I AndroidRuntime: Using default boot image
11-17 14:59:19.193  7080  7080 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:19.286  7080  7080 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:20.358  7080  7080 D AndroidRuntime: Shutting down VM
11-17 14:59:25.351  7108  7108 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:25.355  7108  7108 I AndroidRuntime: Using default boot image
11-17 14:59:25.355  7108  7108 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:25.450  7108  7108 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:26.520  7108  7108 D AndroidRuntime: Shutting down VM
11-17 14:59:31.493  7132  7132 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:31.497  7132  7132 I AndroidRuntime: Using default boot image
11-17 14:59:31.497  7132  7132 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:31.592  7132  7132 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:32.647  7132  7132 D AndroidRuntime: Shutting down VM
11-17 14:59:37.633  7159  7159 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:37.637  7159  7159 I AndroidRuntime: Using default boot image
11-17 14:59:37.637  7159  7159 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:37.733  7159  7159 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:38.800  7159  7159 D AndroidRuntime: Shutting down VM
11-17 14:59:43.796  7182  7182 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:43.800  7182  7182 I AndroidRuntime: Using default boot image
11-17 14:59:43.800  7182  7182 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:43.903  7182  7182 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:44.966  7182  7182 D AndroidRuntime: Shutting down VM
11-17 14:59:49.953  7205  7205 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:49.957  7205  7205 I AndroidRuntime: Using default boot image
11-17 14:59:49.957  7205  7205 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:50.054  7205  7205 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:51.132  7205  7205 D AndroidRuntime: Shutting down VM
11-17 14:59:56.128  7333  7333 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:59:56.133  7333  7333 I AndroidRuntime: Using default boot image
11-17 14:59:56.133  7333  7333 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:59:56.246  7333  7333 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:59:57.298  7333  7333 D AndroidRuntime: Shutting down VM
11-17 14:59:58.969   521   574 I AppsFilter: interaction: PackageSetting{dc90c7e com.ghprotocol.app/10192} -> PackageSetting{3950e9a com.google.android.contacts/10155} BLOCKED
11-17 15:00:02.336  7378  7378 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:02.340  7378  7378 I AndroidRuntime: Using default boot image
11-17 15:00:02.340  7378  7378 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:02.438  7378  7378 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:03.493  7378  7378 D AndroidRuntime: Shutting down VM
11-17 15:00:08.470  7409  7409 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:08.474  7409  7409 I AndroidRuntime: Using default boot image
11-17 15:00:08.474  7409  7409 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:08.571  7409  7409 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:08.983   521   574 I AppsFilter: interaction: PackageSetting{dc90c7e com.ghprotocol.app/10192} -> PackageSetting{dd1dd3e com.google.android.contacts/10155} BLOCKED
11-17 15:00:09.630  7409  7409 D AndroidRuntime: Shutting down VM
11-17 15:00:14.626  7444  7444 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:14.630  7444  7444 I AndroidRuntime: Using default boot image
11-17 15:00:14.630  7444  7444 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:14.731  7444  7444 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:15.808  7444  7444 D AndroidRuntime: Shutting down VM
11-17 15:00:20.788  7472  7472 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:20.792  7472  7472 I AndroidRuntime: Using default boot image
11-17 15:00:20.792  7472  7472 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:20.889  7472  7472 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:21.967  7472  7472 D AndroidRuntime: Shutting down VM
11-17 15:00:26.960  7497  7497 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:26.964  7497  7497 I AndroidRuntime: Using default boot image
11-17 15:00:26.964  7497  7497 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:27.060  7497  7497 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:28.120  7497  7497 D AndroidRuntime: Shutting down VM
11-17 15:00:33.103  7520  7520 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:33.107  7520  7520 I AndroidRuntime: Using default boot image
11-17 15:00:33.107  7520  7520 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:33.200  7520  7520 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:34.268  7520  7520 D AndroidRuntime: Shutting down VM
11-17 15:00:39.241  7543  7543 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:39.245  7543  7543 I AndroidRuntime: Using default boot image
11-17 15:00:39.245  7543  7543 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:39.343  7543  7543 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:40.420  7543  7543 D AndroidRuntime: Shutting down VM
11-17 15:00:45.398  7566  7566 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:45.402  7566  7566 I AndroidRuntime: Using default boot image
11-17 15:00:45.402  7566  7566 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:45.494  7566  7566 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:46.542  7566  7566 D AndroidRuntime: Shutting down VM
11-17 15:00:51.520  7590  7590 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:51.524  7590  7590 I AndroidRuntime: Using default boot image
11-17 15:00:51.524  7590  7590 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:51.624  7590  7590 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:52.692  7590  7590 D AndroidRuntime: Shutting down VM
11-17 15:00:57.693  7619  7619 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:00:57.697  7619  7619 I AndroidRuntime: Using default boot image
11-17 15:00:57.697  7619  7619 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:00:57.793  7619  7619 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:00:58.848  7619  7619 D AndroidRuntime: Shutting down VM
11-17 15:01:03.826  7642  7642 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:03.830  7642  7642 I AndroidRuntime: Using default boot image
11-17 15:01:03.830  7642  7642 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:03.926  7642  7642 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:04.977  7642  7642 D AndroidRuntime: Shutting down VM
11-17 15:01:09.948  7665  7665 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:09.952  7665  7665 I AndroidRuntime: Using default boot image
11-17 15:01:09.952  7665  7665 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:10.046  7665  7665 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:11.111  7665  7665 D AndroidRuntime: Shutting down VM
11-17 15:01:16.087  7690  7690 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:16.092  7690  7690 I AndroidRuntime: Using default boot image
11-17 15:01:16.092  7690  7690 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:16.187  7690  7690 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:17.241  7690  7690 D AndroidRuntime: Shutting down VM
11-17 15:01:22.260  7713  7713 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:22.265  7713  7713 I AndroidRuntime: Using default boot image
11-17 15:01:22.265  7713  7713 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:22.377  7713  7713 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:23.453  7713  7713 D AndroidRuntime: Shutting down VM
11-17 15:01:28.451  7738  7738 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:28.455  7738  7738 I AndroidRuntime: Using default boot image
11-17 15:01:28.455  7738  7738 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:28.552  7738  7738 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:29.615  7738  7738 D AndroidRuntime: Shutting down VM
11-17 15:01:34.626  7761  7761 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:34.630  7761  7761 I AndroidRuntime: Using default boot image
11-17 15:01:34.630  7761  7761 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:34.733  7761  7761 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:35.808  7761  7761 D AndroidRuntime: Shutting down VM
11-17 15:01:40.790  7791  7791 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:40.794  7791  7791 I AndroidRuntime: Using default boot image
11-17 15:01:40.794  7791  7791 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:40.888  7791  7791 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:41.956  7791  7791 D AndroidRuntime: Shutting down VM
11-17 15:01:46.935  7814  7814 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:46.939  7814  7814 I AndroidRuntime: Using default boot image
11-17 15:01:46.939  7814  7814 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:47.036  7814  7814 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:48.108  7814  7814 D AndroidRuntime: Shutting down VM
11-17 15:01:53.096  7837  7837 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:53.100  7837  7837 I AndroidRuntime: Using default boot image
11-17 15:01:53.100  7837  7837 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:53.204  7837  7837 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:01:54.250  7837  7837 D AndroidRuntime: Shutting down VM
11-17 15:01:59.246  7864  7864 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:01:59.250  7864  7864 I AndroidRuntime: Using default boot image
11-17 15:01:59.250  7864  7864 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:01:59.347  7864  7864 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:00.416  7864  7864 D AndroidRuntime: Shutting down VM
11-17 15:02:05.393  7894  7894 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:05.397  7894  7894 I AndroidRuntime: Using default boot image
11-17 15:02:05.397  7894  7894 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:05.493  7894  7894 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:06.548  7894  7894 D AndroidRuntime: Shutting down VM
11-17 15:02:11.527  7919  7919 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:11.531  7919  7919 I AndroidRuntime: Using default boot image
11-17 15:02:11.531  7919  7919 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:11.628  7919  7919 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:12.699  7919  7919 D AndroidRuntime: Shutting down VM
11-17 15:02:17.692  7942  7942 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:17.696  7942  7942 I AndroidRuntime: Using default boot image
11-17 15:02:17.696  7942  7942 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:17.793  7942  7942 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:18.861  7942  7942 D AndroidRuntime: Shutting down VM
11-17 15:02:23.844  7965  7965 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:23.847  7965  7965 I AndroidRuntime: Using default boot image
11-17 15:02:23.847  7965  7965 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:23.942  7965  7965 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:24.995  7965  7965 D AndroidRuntime: Shutting down VM
11-17 15:02:29.982  7990  7990 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:29.986  7990  7990 I AndroidRuntime: Using default boot image
11-17 15:02:29.986  7990  7990 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:30.089  7990  7990 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:31.141  7990  7990 D AndroidRuntime: Shutting down VM
11-17 15:02:36.110  8013  8013 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:36.114  8013  8013 I AndroidRuntime: Using default boot image
11-17 15:02:36.114  8013  8013 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:36.206  8013  8013 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:37.261  8013  8013 D AndroidRuntime: Shutting down VM
11-17 15:02:42.236  8036  8036 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:42.241  8036  8036 I AndroidRuntime: Using default boot image
11-17 15:02:42.241  8036  8036 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:42.338  8036  8036 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:43.402  8036  8036 D AndroidRuntime: Shutting down VM
11-17 15:02:48.376  8059  8059 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:48.381  8059  8059 I AndroidRuntime: Using default boot image
11-17 15:02:48.381  8059  8059 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:48.474  8059  8059 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:49.538  8059  8059 D AndroidRuntime: Shutting down VM
11-17 15:02:54.505  8082  8082 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:02:54.508  8082  8082 I AndroidRuntime: Using default boot image
11-17 15:02:54.508  8082  8082 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:02:54.605  8082  8082 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:02:55.681  8082  8082 D AndroidRuntime: Shutting down VM
11-17 15:03:00.675  8108  8108 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:03:00.679  8108  8108 I AndroidRuntime: Using default boot image
11-17 15:03:00.679  8108  8108 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:03:00.775  8108  8108 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:03:01.830  8108  8108 D AndroidRuntime: Shutting down VM
11-17 15:03:06.792  8131  8131 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:03:06.796  8131  8131 I AndroidRuntime: Using default boot image
11-17 15:03:06.796  8131  8131 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:03:06.890  8131  8131 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:03:07.937  8131  8131 D AndroidRuntime: Shutting down VM
11-17 15:03:12.920  8154  8154 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:03:12.924  8154  8154 I AndroidRuntime: Using default boot image
11-17 15:03:12.924  8154  8154 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:03:13.017  8154  8154 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:03:14.085  8154  8154 D AndroidRuntime: Shutting down VM
11-17 15:03:19.047  8197  8197 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:03:19.051  8197  8197 I AndroidRuntime: Using default boot image
11-17 15:03:19.051  8197  8197 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:03:19.145  8197  8197 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:03:20.223  8197  8197 D AndroidRuntime: Shutting down VM
11-17 15:03:25.205  8220  8220 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:03:25.209  8220  8220 I AndroidRuntime: Using default boot image
11-17 15:03:25.209  8220  8220 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:03:25.305  8220  8220 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:03:26.395  8220  8220 D AndroidRuntime: Shutting down VM


